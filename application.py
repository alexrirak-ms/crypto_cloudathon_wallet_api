import psycopg2 as psycopg2
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os, sys

app = Flask(__name__)
CORS(app)

'''
This the the root entry file. Only things that need to be centrally accessible should be defined here
'''

# CONSTANTS
BLOCKCYPHER_API_KEY = os.getenv("BLOCKCYPHER_API_KEY", "NO API KEY SET")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_SCHM = os.getenv("DATABASE_SCHM")


def get_db_connection():
    """
    Helper method to return a DB Connection handle
    :return:
    """
    return psycopg2.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASS,
        dbname=DATABASE_SCHM
    )


def get_string_from_file(file_path: str) -> str:
    """
    Helper method to read a file in as a string
    :param file_path: the path to the file
    :return: string representation of the file
    """
    with open(file_path, 'r') as file:
        return file.read()


# import routes from other files
import wallet_routes
import transaction_routes
import user_routes

# Load env vars
load_dotenv()

# Make sure the env vars we expect are set
if DATABASE_HOST is None or \
        DATABASE_USER is None or \
        DATABASE_PASS is None or \
        DATABASE_SCHM is None:
    print("*** Missing environment variables ***")
    sys.exit()
