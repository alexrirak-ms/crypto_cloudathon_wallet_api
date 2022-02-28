# Convert to USD

Converts the given amount of coin into its USD value

**URL** : `/conversions/to-usd/:symbol/:amount`

**URL Parameters** : 
 - `symbol=[string]` where `symbol` is the symbol of the coin in the database.
 - `amount=[int]` where `amount` is the amount of the coin in the lowest non-divisible unit (ex satoshi).

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```text
{
    "convertedCoin": "bcy",
    "inputAmount": 100000000,
    "usdValue": 39741.65
}
```