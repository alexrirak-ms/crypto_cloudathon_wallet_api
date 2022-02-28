# Wallet / Transaction API
The source code for the wallet and transaction APIs. Hosted as a single flask.

[![Build and deploy to Azure Web App - crypto-banksters-wallet-api](https://github.com/alexrirak-ms/crypto_cloudathon_wallet_api/actions/workflows/main_crypto-banksters-wallet-api.yml/badge.svg)](https://github.com/alexrirak-ms/crypto_cloudathon_wallet_api/actions/workflows/main_crypto-banksters-wallet-api.yml)

## Running Locally
Install python dependencies and run flask app as normal. PyCharm run configuration is also provided. 
*Also see the environment setup section below*
```
pip install -r requirements.txt
set FLASK_APP=application
flask run
```
Please note, one of the pre-requisites is pg_config which is installed by installing the PostGresSQL client


### Environment Setup
To run this locally you need to have the proper environment variables set. `dotenv` is used to make this easy.
Create a new file in the root directory called `.env` and populate it with the following keys and add in the values
````
BLOCKCYPHER_API_KEY=
DATABASE_HOST=
DATABASE_USER=
DATABASE_PASS=
DATABASE_SCHM=
APPLICATIONINSIGHTS_CONNECTION_STRING=
````

## API Docs

### Transaction API
[Azure Link](https://crypto-banksters-wallet-api.azurewebsites.net/transaction)

Endpoints which manipulate or display information related to transactions:

* [Health Ping](docs/transaction/transaction.md) : `GET /transaction`
* [Get Transaction](docs/transaction/get_transaction.md) : `GET /transaction/:coin/:transaction_hash`
* [Create Transaction](docs/transaction/create_transaction.md) : `PUT /transaction`
* [Create Funding Transaction](docs/transaction/create_funding_transaction.md) : `POST /transaction/fund/:wallet_id/:amount`
* [Get Value in USD](docs/transaction/get_value_in_usd.md) : `GET /conversions/usd-value/:symbol`
* [Convert to USD](docs/transaction/get_value_to_usd.md) : `GET /conversions/to-usd/:symbol/:amount`
* [Convert from USD](docs/transaction/get_value_from_usd.md) : `GET /conversions/from-usd/:symbol/:amount`

### Wallet API
[Azure Link](https://crypto-banksters-wallet-api.azurewebsites.net/wallet)

Endpoints which manipulate or display information related to wallets:

* [Health Ping](docs/wallet/wallet.md) : `GET /wallet`
* [Get Wallet Details](docs/wallet/get_wallet.md) : `GET /wallet/:wallet_id`
* [Get All Wallet Details By User](docs/wallet/get_wallets_by_user.md) : `GET /wallets/user/:user_id`
* [Get Wallet Value](docs/wallet/get_wallet_value.md) : `GET /wallet/:wallet_id/value`
* [Create Wallet](docs/wallet/create_wallet.md) : `PUT /wallets/:chain_id/:user_id`

### User API
[Azure Link](https://crypto-banksters-wallet-api.azurewebsites.net/user)

Endpoints which manipulate or display information related to users:

* [Health Ping](docs/user/user.md) : `GET /user`
* [Get User By Id](docs/user/get_user_by_id.md) : `GET /user/:user_id`
* [Get User By Username](docs/user/get_user_by_username.md) : `GET /user/by-username/:username`