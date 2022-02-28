import json
import logging
import sys
import uuid
from datetime import datetime

import blockcypher
import requests
from flask import request, abort
from opencensus.ext.azure.log_exporter import AzureLogHandler
from requests import ReadTimeout

from application import app, BLOCKCYPHER_API_KEY, get_db_connection, get_string_from_file, tracer

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Export logs + traces to azure insights
logger.addHandler(AzureLogHandler())


@app.route('/transaction')
def transaction():
    return "Hello Transaction"


@app.route('/transaction/<string:coin>/<string:transaction_hash>')
def get_transaction(coin: str, transaction_hash: str):
    """
    Fetches transaction details from the blockchain based on specified coin/hash
    :param coin: coin representation as per blockcypher (bcy for bitcoin test chain)
    :param transaction_hash: the hash of a transaction of the blockchain
    :return: the raw transaction details as per blockcypher
        (see https://www.blockcypher.com/dev/bitcoin/#transaction-hash-endpoint)
    """

    try:
        transaction_details = blockcypher.get_transaction_details(transaction_hash,
                                                                  coin_symbol=coin,
                                                                  api_key=BLOCKCYPHER_API_KEY)

        if 'error' in transaction_details:
            logger.warning("Could not find transaction {} on {} chain".format(transaction_hash, coin))
            abort(404)

        return (transaction_details, 200)
    except AssertionError:
        logger.error("Could not fetch transaction details from BlockCypher")
        abort(400, "Error from Blockcypher API")


@app.route('/transaction', methods=['PUT'])
def create_transaction():
    """
    Creates a transaction
    Expects to receive a json body containing
        fromWalletId: id of the wallet in the DB from which to send the money
        toAddress: this is a wallet address on the proper chain (assumed to be correct 🤞)
        amount: the amount to send (in the lowest non-divisible unit - satoshi, gwei, etc)
    :return: json object with the transaction_id and status of the created transaction
    """

    # validate the request
    if not request.json \
            or not 'fromWalletId' in request.json \
            or not 'toAddress' in request.json \
            or not 'amount' in request.json \
            or int(request.json['amount']) < 1:
        logger.error('Received invalid request \n {} \n'.format(request.json))
        abort(400)

    logger.info('Creating new transaction from {}'.format(request.json['fromWalletId']))

    wallet_details_response = get_wallet_details_by_id(request.json['fromWalletId'])

    logger.info('Fetched wallet details {}'.format(wallet_details_response))

    # fetch the private key from db - api does not return that (we're semi-secure 😁)
    with get_db_connection() as db:
        with db.cursor() as cursor:
            # fetch the private key for the wallet
            cursor.execute(GET_WALLET_PRIVATE_KEY_BY_ID % (request.json['fromWalletId']))
            result = cursor.fetchone()

            if result is None:
                abort(400, "Unknown Wallet id")

            logger.info('Fetched wallet private key')

            transaction_hash = ""
            # Use teh blockcypher api to initiate the transaction
            try:
                transaction_hash = blockcypher.simple_spend(
                    from_privkey=result[0],
                    to_address=request.json['toAddress'],
                    to_satoshis=request.json['amount'],
                    coin_symbol=wallet_details_response['symbol'].lower(),
                    api_key=BLOCKCYPHER_API_KEY)
            except AssertionError:
                logger.error("Could not fetch transaction details from BlockCypher")
                abort(400, "Error from Blockcypher API")

            logger.info('Created transaction with hash {}'.format(transaction_hash))

            transaction_id = str(uuid.uuid4())
            cursor.execute(INSERT_CRYPTO_TRANSACTION_DETAILS, (transaction_id,
                                                               request.json['fromWalletId'],
                                                               wallet_details_response['chain_id'],
                                                               transaction_hash,
                                                               datetime.now(),
                                                               None,
                                                               "Pending"))
            db.commit()

            logger.info('Persisted transaction in db with id {}'.format(transaction_id))

            return ({"transaction_id": transaction_id, "status": "Pending"}, 201)


@app.route('/transaction/fund/<string:wallet_id>/<int:amount>', methods=['POST'])
def create_funding_transaction(wallet_id: str, amount: int):
    """
    creates a funding transaction using a test faucet
    :param wallet_id: internal wallet if of wallet to fund
    :param amount: the amount to send (in the lowest non-divisible unit - satoshi)
    :return: json object with the transaction hash from the blockchain (transactionHash)
    """

    wallet_details_response = get_wallet_details_by_id(wallet_id)

    # the faucet only work for the BTC test chain (BCY)
    if wallet_details_response['symbol'].lower() != 'bcy':
        abort(400, "Funding not available on this chain")

    # the faucet will fund not fund more than 100 million BlockCypher satoshis at a time
    if amount > 100000000:
        abort(400, "Fund amount too high")

    if amount < 1:
        abort(400, "Fund amount too low")

    try:
        fundingTxn = blockcypher.send_faucet_coins(address_to_fund=wallet_details_response['public_address'],
                                                   satoshis=amount,
                                                   coin_symbol=wallet_details_response['symbol'].lower(),
                                                   api_key=BLOCKCYPHER_API_KEY)

        return ({"transactionHash": fundingTxn['tx_ref']}, 201)

    except AssertionError:
        logger.error("Could not create funding transaction via BlockCypher")
        abort(400, "Error from Blockcypher API")


@app.route('/conversions/usd-value/<string:symbol>')
def get_value_in_usd(symbol: str) -> str:
    """
    Fetches the USD value of a coin
    :param symbol: the symbol of the coin
    :return: string representation of the price
    """
    symbol = symbol.lower()

    # The test chain doesnt have separate valuation
    if symbol == 'bcy':
        symbol = 'btc'

    url = "https://data.messari.io/api/v1/assets/{}/metrics/market-data".format(symbol)

    with tracer.span(name='parent'):
        response = requests.get(url)

        if response.status_code != 200:
            logger.error("Could not create fetch usd value via messari")
            abort(400, "Error from Messari API")

        crypto_data = json.loads(response.content)
        value_in_usd = crypto_data['data']['market_data']['price_usd']

        return str(value_in_usd)


# Deprecated, use /conversions/usd-value/<string:symbol> instead
@app.route('/usd-value/<string:symbol>')
def get_value_in_usd_old(symbol: str) -> str:
    """
    Fetches the USD value of a coin (DEPRECATED)
    :param symbol: the symbol of the coin
    :return: string representation of the price
    """
    return get_value_in_usd(symbol)


@app.route('/conversions/to-usd/<string:symbol>/<int:amount>')
def get_value_to_usd(symbol: str, amount: int) -> str:
    """
    Returns the value in us dollars of the given coin and amount
    :param symbol: the coin being converted
    :param amount: (in the lowest non-divisible unit - satoshi)
    :return:
    """
    return ({
                "usdValue": round(amount / 100000000 * float(get_value_in_usd_old(symbol)), 2),
                "convertedCoin": symbol,
                "inputAmount": amount
            }, 200)


def get_wallet_details_by_id(wallet_id: str):
    """
    fetches the wallet details from the wallet API
    :param wallet_id: internal wallet id
    :return: json object of wallet details
        chain_id, name, public_address, public_key, symbol, user_id, wallet_id
    """

    # fetch wallet details from wallet api
    url = request.url_root + "wallet/" + wallet_id
    logger.info("Fetching wallet details for {} at {}".format(wallet_id, url))

    try:
        wallet_details_response = requests.get(url, timeout=10)

        if wallet_details_response.status_code != 200:
            logger.error('Could not fetch wallet details for {} \n {}'.format(wallet_id, wallet_details_response.text))
            abort(500, "Non 200 response from wallet api")

        return json.loads(wallet_details_response.text)
    except ReadTimeout:
        logger.error('Timed out waiting for wallet details for {}'.format(wallet_id))
        abort(500, "Timed out waiting on wallet api")


# Define all our queries here cause python doesn't like me doing this on top
GET_WALLET_PRIVATE_KEY_BY_ID = get_string_from_file('sql/getWalletPrivateKeyById.sql')
INSERT_CRYPTO_TRANSACTION_DETAILS = get_string_from_file('sql/insertCryptoTransactionDetails.sql')
