import blockcypher
from flask import request

from application import app, BLOCKCYPHER_API_KEY, get_db_connection, get_string_from_file


@app.route('/transaction')
def transaction():
    return "Hello Transaction"


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

    with get_db_connection() as db:
        with db.cursor() as cursor:
            cursor.execute(GET_WALLET_PRIVATE_KEY_BY_ID % (request.json['fromWalletId']))
            result = cursor.fetchone()

            transaction_hash = blockcypher.simple_spend(
                from_privkey=result[0],
                to_address=request.json['toAddress'],
                to_satoshis=request.json['amount'],
                coin_symbol='bcy',
                api_key=BLOCKCYPHER_API_KEY)

            return {"transactionHash": transaction_hash}


# Define all our queries here cause python doesn't like me doing this on top
GET_WALLET_PRIVATE_KEY_BY_ID = get_string_from_file('sql/getWalletPrivateKeyById.sql')
