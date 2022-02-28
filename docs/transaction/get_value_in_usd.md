# Get Value in USD

Fetches the USD value of a coin based on *messari.io* api. *(Handles test chain symbol internally)*

**URL** : `/conversions/usd-value/:symbol`

**URL Parameters** : `symbol=[string]` where `symbol` is the symbol of the coin in the database.

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```text
{
    "coin": "btc",
    "usdPrice": 39962.92937321809
}
```