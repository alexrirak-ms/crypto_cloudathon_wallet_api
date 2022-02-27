# Wallet / Transaction API
The source code for the wallet and transaction APIs. Hosted as a single flask.

[![Build and deploy to Azure Web App - crypto-banksters-wallet-api](https://github.com/alexrirak-ms/crypto_cloudathon_wallet_api/actions/workflows/main_crypto-banksters-wallet-api.yml/badge.svg)](https://github.com/alexrirak-ms/crypto_cloudathon_wallet_api/actions/workflows/main_crypto-banksters-wallet-api.yml)

## Transaction API
[Azure Link](https://crypto-banksters-wallet-api.azurewebsites.net/transaction)

## Wallet API
[Azure Link](https://crypto-banksters-wallet-api.azurewebsites.net/wallet)

Endpoints which manipulate or display information related to wallets:

* [Health Ping](docs/wallet/wallet.md) : `GET /wallet`
* [Get Wallet Details](docs/wallet/get_wallet.md) : `GET /wallet/:wallet_id`
* [Get All Wallet Details By User](docs/wallet/get_wallets_by_user.md) : `GET /wallets/user/:user_id`
* [Get Wallet Value](docs/wallet/get_wallet_value.md) : `GET /wallet/:wallet_id/value`
* [Create Wallet](docs/wallet/create_wallet.md) : `PUT /wallets/:chain_id/:user_id`