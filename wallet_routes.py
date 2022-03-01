import json
import logging
import sys
import uuid

import blockcypher

from application import app, get_string_from_file, get_db_connection, BLOCKCYPHER_API_KEY
from opencensus.ext.azure.log_exporter import AzureLogHandler

from flask import abort, request

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Export logs + traces to azure insights
logger.addHandler(AzureLogHandler())

@app.route('/wallet')
def wallet():
    return "Hello Wallet"


@app.route('/wallet/<string:wallet_id>')
def get_wallet(wallet_id: str, ):
    """
    Fetches wallet details based on id
    :param wallet_id: the wallet id to fetch
    :return: json object of wallet details
        chain_id, name, public_address, public_key, symbol, user_id, wallet_id
    """
    if wallet_id is None:
        abort(400, "Invalid Request")

    logger.info("Fetching wallet with id {}".format(wallet_id))

    with get_db_connection() as db:
        with db.cursor() as cursor:
            # fetch the private key for the wallet
            cursor.execute(GET_WALLET_DETAILS_BY_ID % (wallet_id))

            try:
                # maps the column names onto the result giving us a dictionary and thus json friendly object
                columns = cursor.description
                result = [{columns[index][0]: column for index, column in enumerate(value)}
                          for value in cursor.fetchall()]

                if result is None:
                    logger.error("Could not find wallet with id {}".format(wallet_id))
                    abort(400, "Unknown Wallet id")

                return (result[0], 200)
            except IndexError:
                logger.error("Could not find wallet with id {}".format(wallet_id))
                abort(400, "Could not fetch wallet details")


@app.route('/wallets/user/<string:user_id>')
def get_wallets_by_user(user_id: str):
    """
    Fetches wallet details based on user_id
    :param user_id: the id of the wallet owner
    :return: json object list of wallet details
        chain_id, name, public_address, public_key, symbol, user_id, wallet_id
        If query param include_values=True also returns confirmed_balance, unconfirmed_balance, total_balance
    """
    if user_id is None:
        abort(400, "Invalid Request")

    # check if query param include_values is set
    include_values = request.args.get("include_values", default=False, type=bool)

    with get_db_connection() as db:
        with db.cursor() as cursor:
            # fetch the private key for the wallet
            cursor.execute(GET_WALLETS_BY_USER % (user_id))

            try:
                # maps the column names onto the result giving us a dictionary and thus json friendly object
                columns = cursor.description
                result = [{columns[index][0]: column for index, column in enumerate(value)}
                          for value in cursor.fetchall()]

                if result is None or not result:
                    abort(400, "Unknown User id")

                # if we need values, fetch them using our other method
                if include_values:
                    for item in result:
                        item["balances"] = get_wallet_value(item["wallet_id"])[0]

                return (json.dumps(result), 200)
            except IndexError:
                abort(400, "Could not fetch wallet info")


@app.route('/wallet/<string:wallet_id>/value')
def get_wallet_value(wallet_id: str):
    """
    Given a wallet id fetches its balance from the blockchain
    :param wallet_id: the wallet id to fetch
    :return: json object of wallet balances (in the lowest non-divisible unit - satoshi, gwei, etc)
        confirmed_balance, unconfirmed_balance, total_balance
    """
    if wallet_id is None:
        abort(400, "Invalid Request")

    wallet_details = get_wallet(wallet_id)[0]

    address_details = blockcypher.get_address_overview(wallet_details['public_address'],
                                                       coin_symbol=wallet_details['symbol'].lower(),
                                                       api_key=BLOCKCYPHER_API_KEY)

    return ({
        "confirmed_balance": address_details['balance'],
        "unconfirmed_balance": address_details['unconfirmed_balance'],
        "total_balance": address_details['final_balance']
    }, 200)


@app.route('/wallet/<string:chain_id>/<string:user_id>', methods=['PUT'])
def create_wallet(chain_id: str, user_id: str):
    """
    Creates a wallet on the given chain belonging to the given user
    :param chain_id: the chain on which to create an account
    :param user_id: the owner of the new wallet
    :return: json object of wallet details
        chain_id, name, public_address, public_key, symbol, user_id, wallet_id
    """

    if chain_id is None:
        abort(400, "Coin not specified")

    if user_id is None:
        abort(400, "User not specified")

    logger.info("Creating wallet for {} on chain {}".format(user_id, chain_id))

    with get_db_connection() as db:
        with db.cursor() as cursor:
            # get info on the chain
            cursor.execute(GET_CHAIN_INFO_BY_ID % (chain_id))

            # maps the column names onto the result giving us a dictionary and thus json friendly object
            columns = cursor.description
            chain_info = {}

            try:
                chain_info = [{columns[index][0]: column for index, column in enumerate(value)}
                              for value in cursor.fetchall()]

                if chain_info is None or not chain_info:
                    abort(400, "Unknown chain id")

            except IndexError:
                abort(400, "Could not find chain id")

            chain_info = chain_info[0]

            # Create a new wallet using blockcypher api
            new_wallet = blockcypher.generate_new_address(coin_symbol=chain_info['symbol'].lower(),
                                                          api_key=BLOCKCYPHER_API_KEY)

            # generate uuids for our db entries
            connection_id = str(uuid.uuid4())
            wallet_id = str(uuid.uuid4())

            # insert connection details and wallet as a single transaction
            cursor.execute(INSERT_CONNECTION_DETAILS, (connection_id,
                                                       new_wallet['address'],
                                                       new_wallet['public'],
                                                       new_wallet['private'],
                                                       chain_id))
            cursor.execute(INSERT_WALLET_DETAILS, (wallet_id,
                                                   user_id,
                                                   connection_id))
            db.commit()

            # fetch the wallet as it should now be in the db
            return (get_wallet(wallet_id)[0], 201)

    # we should never get here
    abort(500, "Unknown error")


# Define all our queries here cause python doesn't like me doing this on top
GET_WALLET_DETAILS_BY_ID = get_string_from_file('sql/getWalletDetailsById.sql')
GET_WALLETS_BY_USER = get_string_from_file('sql/getWalletsByUser.sql')
GET_CHAIN_INFO_BY_ID = get_string_from_file('sql/getChainInfoById.sql')
INSERT_CONNECTION_DETAILS = get_string_from_file('sql/insertConnectionDetails.sql')
INSERT_WALLET_DETAILS = get_string_from_file('sql/insertWalletDetails.sql')
