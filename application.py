from flask import Flask

app = Flask(__name__)

'''
This the the root entry file. Only things that need to be centrally accessible should be defined here
'''

# import routes from other files
import wallet_routes
import transaction_routes

