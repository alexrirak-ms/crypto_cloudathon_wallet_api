# Get Wallet

Fetches wallet details based on wallet id

**URL** : `/wallet/:wallet_id`

**URL Parameters** : `wallet_id=[string]` where `wallet_id` is the ID of the Wallet in the
database.

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "chain_id": "abd76ab0-0b3c-4d33-84f2-5582f482acd3",
    "name": "Bitcoin (Test Net)",
    "public_address": "C2zfwTM9uWuMUA3zssbXRHgPJhKpUeWBd1",
    "public_key": "038d3282aa146e680939aaa7896d68614994867e7b1c37672674c8cb47ba33b671",
    "symbol": "BCY",
    "user_id": "e16666ff-c559-4aab-96eb-f0a5c2c77b18",
    "wallet_id": "cd6076fc-e4bc-4f34-800b-1fdf8c64e884"
}
```