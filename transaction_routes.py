from datetime import datetime
import json
import logging
import uuid

import blockcypher
import requests
from flask import request, abort

from application import app, BLOCKCYPHER_API_KEY, get_db_connection, get_string_from_file


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
    transaction_details = blockcypher.get_transaction_details(transaction_hash,
                                                              coin_symbol=coin,
                                                              api_key=BLOCKCYPHER_API_KEY)

    if 'error' in transaction_details:
        logging.warning("Could not find transaction {} on {} chain".format(transaction_hash, coin))
        abort(404)

    return (transaction_details, 200)


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
            or not 'amount' in request.json:
        logging.error('Received invalid request \n {} \n'.format(request.json))
        abort(400)

    logging.info('Creating new transaction from {}'.format(request.json['fromWalletId']))

    wallet_details_response = get_wallet_details_by_id(request.json['fromWalletId'])

    # fetch the private key from db - api does not return that (we're semi-secure 😁)
    with get_db_connection() as db:
        with db.cursor() as cursor:
            # fetch the private key for the wallet
            cursor.execute(GET_WALLET_PRIVATE_KEY_BY_ID % (request.json['fromWalletId']))
            result = cursor.fetchone()

            if result is None:
                abort(400, "Unknown Wallet id")

            # Use teh blockcypher api to initiate the transaction
            transaction_hash = blockcypher.simple_spend(
                from_privkey=result[0],
                to_address=request.json['toAddress'],
                to_satoshis=request.json['amount'],
                coin_symbol=wallet_details_response['symbol'].lower(),
                api_key=BLOCKCYPHER_API_KEY)

            transaction_id = str(uuid.uuid4())
            cursor.execute(INSERT_CRYPTO_TRANSACTION_DETAILS, (transaction_id,
                                                               request.json['fromWalletId'],
                                                               wallet_details_response['chain_id'],
                                                               transaction_hash,
                                                               datetime.now(),
                                                               None,
                                                               "Pending"))
            db.commit()

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

    fundingTxn = blockcypher.send_faucet_coins(address_to_fund=wallet_details_response['public_address'],
                                               satoshis=amount,
                                               coin_symbol=wallet_details_response['symbol'].lower(),
                                               api_key=BLOCKCYPHER_API_KEY)

    return ({"transactionHash": fundingTxn['tx_ref']}, 201)


def get_wallet_details_by_id(wallet_id: str):
    """
    fetches the wallet details from the wallet API
    :param wallet_id: internal wallet id
    :return: json object of wallet details
        chain_id, name, public_address, public_key, symbol, user_id, wallet_id
    """

    # fetch wallet details from wallet api
    wallet_details_response = requests.get(request.url_root + "/wallet/" + wallet_id)

    if wallet_details_response.status_code != 200:
        logging.error('Could not fetch wallet details for {}'.format(wallet_id))
        abort(400)

    return json.loads(wallet_details_response.text)


# Define all our queries here cause python doesn't like me doing this on top
GET_WALLET_PRIVATE_KEY_BY_ID = get_string_from_file('sql/getWalletPrivateKeyById.sql')
INSERT_CRYPTO_TRANSACTION_DETAILS = get_string_from_file('sql/insertCryptoTransactionDetails.sql')
