import logging
import sys
import uuid

from application import app, get_string_from_file, get_db_connection
from flask import abort, request
from opencensus.ext.azure.log_exporter import AzureLogHandler

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.INFO)

logger = logging.getLogger(__name__)
streamHandler = logging.StreamHandler(sys.stdout)

logger.addHandler(AzureLogHandler())


@app.route('/user')
def user():
    return "Hello User"


@app.route('/user/<string:user_id>')
def get_user_by_id(user_id: str):
    """
    fetches a user by user_id
    :param user_id: id of the user to fetch
    :return: json object of the user's properties
        user_id, email, username
    """
    if user_id is None:
        abort(400, "Missing User_id")

    with get_db_connection() as db:
        with db.cursor() as cursor:
            # fetch the private key for the wallet
            cursor.execute(GET_USER_INFO_BY_ID % (user_id))

            try:
                # maps the column names onto the result giving us a dictionary and thus json friendly object
                columns = cursor.description
                result = [{columns[index][0]: column for index, column in enumerate(value)}
                          for value in cursor.fetchall()]

                if result is None:
                    abort(400, "Could not find user")

                return (result[0], 200)
            except IndexError:
                abort(400, "Could not find user")


@app.route('/user/by-username/<string:username>')
def get_user_by_username(username: str):
    """
    Fetches a user by username
    If query param create_user=True will create the user if it doesn't exist
    :param username: id of the user to fetch
    :return: json object of the user's properties
        user_id, email, username
    """
    if username is None:
        abort(400, "Missing Username")

    # check if query param include_values is set
    create_new = request.args.get("create_user", default=False, type=bool)

    with get_db_connection() as db:
        with db.cursor() as cursor:
            # fetch the private key for the wallet
            cursor.execute(GET_USER_INFO_BY_USERNAME % (username))

            try:
                # maps the column names onto the result giving us a dictionary and thus json friendly object
                columns = cursor.description
                result = [{columns[index][0]: column for index, column in enumerate(value)}
                          for value in cursor.fetchall()]

                if result is None:
                    if create_new:
                        logger.info('Could not find user with username {}, creating one'.format(username))
                        return get_user_by_id(create_user(username, username))
                    else:
                        abort(400, "Could not find user")

                return (result[0], 200)
            except IndexError:
                if create_new:
                    logger.info('Could not find user with username {}, creating one'.format(username))
                    return get_user_by_id(create_user(username, username))
                else:
                    abort(400, "Could not find user")


def create_user(username: str, email: str) -> str:
    """
    Creates a user with the given username/email
    :param username:
    :param email:
    :return: user_id of the newly created row
    """
    with get_db_connection() as db:
        with db.cursor() as cursor:
            user_id = str(uuid.uuid4())
            cursor.execute(INSERT_USER_DETAILS, (user_id,
                                                 email,
                                                 username))
            db.commit()

            return user_id


# Define all our queries here cause python doesn't like me doing this on top
GET_USER_INFO_BY_USERNAME = get_string_from_file('sql/getUserInfoByUsername.sql')
GET_USER_INFO_BY_ID = get_string_from_file('sql/getUserInfoById.sql')
INSERT_USER_DETAILS = get_string_from_file('sql/insertUserDetails.sql')
