# Get Wallets By User

Fetches wallet details based on user id

**URL** : `/wallets/user/:user_id`

**URL Parameters** : `user_id=[string]` where `user_id` is the ID of the User in the
database.

**Query Parameters** : `?include_values=[boolean]` where `include_values` specifies whether to include balance details

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
[{
	"wallet_id": "cd6076fc-e4bc-4f34-800b-1fdf8c64e884",
	"user_id": "e16666ff-c559-4aab-96eb-f0a5c2c77b18",
	"chain_id": "abd76ab0-0b3c-4d33-84f2-5582f482acd3",
	"name": "Bitcoin (Test Net)",
	"symbol": "BCY",
	"public_address": "C2zfwTM9uWuMUA3zssbXRHgPJhKpUeWBd1",
	"public_key": "038d3282aa146e680939aaa7896d68614994867e7b1c37672674c8cb47ba33b671"
}]
```

For a request with `?include_values=True`

```json
[{
	"wallet_id": "cd6076fc-e4bc-4f34-800b-1fdf8c64e884",
	"user_id": "e16666ff-c559-4aab-96eb-f0a5c2c77b18",
	"chain_id": "abd76ab0-0b3c-4d33-84f2-5582f482acd3",
	"name": "Bitcoin (Test Net)",
	"symbol": "BCY",
	"public_address": "C2zfwTM9uWuMUA3zssbXRHgPJhKpUeWBd1",
	"public_key": "038d3282aa146e680939aaa7896d68614994867e7b1c37672674c8cb47ba33b671",
	"balances": {
		"confirmed_balance": 97216000,
		"unconfirmed_balance": 0,
		"total_balance": 97216000
	}
}]
```