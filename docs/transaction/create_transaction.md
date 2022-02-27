# Create Transaction

Creates a transaction based on provided parameters. Returns a transaction id for DB lookup

**URL** : `/transaction`

**Method** : `PUT`

**Data constraints**

All fields are required.

```json
{
    "fromWalletId": "[id of the wallet in the DB from which to send]",
    "toAddress": "[public wallet address on the proper chain]",
    "amount": "[the amount to send (in the lowest non-divisible unit - satoshi, gwei, etc)]"
}
```

**Data example** All fields must be sent.

```json
{
    "fromWalletId":"cd6076fc-e4bc-4f34-800b-1fdf8c64e884",
    "toAddress":"BsCBSiUzqnTQgnHrSejfg5ac1syQewExGw",
    "amount":5000
}
```

## Success Response

**Code** : `201 OK`

**Content example**

```json
{
    "status": "Pending",
    "transaction_id": "fa5882bc-7646-47d2-bcff-e6441d6eb38e"
}
```