from application import app, get_string_from_file, get_db_connection

from flask import abort


@app.route('/wallet')
def wallet():
    return "Hello Wallet"


@app.route('/wallet/<string:wallet_id>')
def get_wallet(wallet_id: str,):

    if wallet_id is None:
        abort(400, "Invalid Request")

    with get_db_connection() as db:
        with db.cursor() as cursor:
            # fetch the private key for the wallet
            cursor.execute(GET_WALLET_DETAILS_BY_ID % (wallet_id))

            # maps the column names onto the result giving us a dictionary and thus json friendly object
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)}
                      for value in cursor.fetchall()]

            if result is None:
                abort(400, "Unknown Wallet id")

            return (result[0], 200)


# Define all our queries here cause python doesn't like me doing this on top
GET_WALLET_DETAILS_BY_ID = get_string_from_file('sql/getWalletDetailsById.sql')