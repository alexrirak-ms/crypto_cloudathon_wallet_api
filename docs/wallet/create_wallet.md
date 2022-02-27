# Create Wallet

Creates a wallet on the given chain belonging to the given user

**URL** : `/wallets/:chain_id/:user_id`

**URL Parameters** : 
 - `chain_id=[string]` where `chain_id` is the ID of the Chain in the database.
 - `user_id=[string]` where `user_id` is the ID of the User in the database.

**Method** : `PUT`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "chain_id": "abd76ab0-0b3c-4d33-84f2-5582f482acd3",
    "name": "Bitcoin (Test Net)",
    "public_address": "CBxNVXJx1FEHRHLbbDYAngkUbHwfSCinw1",
    "public_key": "02f91b35657c41aff426e99e3eacf6c30c26efddf6a0cc851453ff889c85b7f3c4",
    "symbol": "BCY",
    "user_id": "5265948e-0ae1-4c2f-a093-4ee742d66507",
    "wallet_id": "61a193db-c932-4c29-b97a-ca208b1488ce"
}
```