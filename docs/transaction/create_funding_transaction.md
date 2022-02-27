# Create Funding Transaction

Creates a funding transaction using a test faucet. *This currently only works for the Bitcoin Testnet (BCY)*

**URL** : `/transaction/fund/:wallet_id/:amount`

**URL Parameters** : 
 - `wallet_id=[string]` where `wallet_id` is the id of the wallet in the DB which is to be funded.
 - `amount=[int]` where `amount` is the amount to send (in the lowest non-divisible unit - satoshi).
 
**Method** : `POST`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "transactionHash": "1509aa2eb9c2de35bb7d4682ba21ae07844daea76e1b21842559c2c83b3a101a"
}
```