import logging

import blockcypher
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
    :return: json object with the transaction hash from the blockchain (transactionHash)
    """
    # TODO: Coin should be determined from wallet type - currently hardcoded

    # validate the request
    if not request.json \
            or not 'fromWalletId' in request.json \
            or not 'toAddress' in request.json \
            or not 'amount' in request.json:
        logging.error('Received invalid request \n {} \n'.format(request.json))
        abort(400)

    logging.info('Creating new transaction from {}'.format(request.json['fromWalletId']))

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
                coin_symbol='bcy',
                api_key=BLOCKCYPHER_API_KEY)

            return ({"transactionHash": transaction_hash}, 201)


# Define all our queries here cause python doesn't like me doing this on top
GET_WALLET_PRIVATE_KEY_BY_ID = get_string_from_file('sql/getWalletPrivateKeyById.sql')
