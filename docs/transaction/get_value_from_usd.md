# Convert from USD

Converts the given amount of USD dollars into its coin value in the lowest non-divisible unit (ex satoshi)

**URL** : `/conversions/from-usd/:symbol/:amount`

**URL Parameters** : 
 - `symbol=[string]` where `symbol` is the symbol of the coin in the database.
 - `amount=[int]` where `amount` is the amount of US dollars.

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```text
{
    "coinValue": 98333927.3969889,
    "convertedCoin": "btc",
    "inputAmount": 40000
}
```