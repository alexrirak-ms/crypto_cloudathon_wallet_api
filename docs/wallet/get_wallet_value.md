# Get Wallet Value

Given a wallet id fetches its balance from the blockchain

**URL** : `/wallet/:wallet_id/value`

**URL Parameters** : `wallet_id=[string]` where `wallet_id` is the ID of the Wallet in the
database.

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "confirmed_balance": 97216000,
    "total_balance": 97216000,
    "unconfirmed_balance": 0
}
```