# Get Transaction

Fetches transaction details from the blockchain based on specified coin/hash

**URL** : `/transaction/:coin/:transaction_hash`

**URL Parameters** : 
 - `coin=[string]` where `coin` is the symbol of the coin in the database.
 - `transaction_hash=[string]` where `transaction_hash` is the hash of the transaction on the blockchain.

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
	"addresses": [
		"BsCBSiUzqnTQgnHrSejfg5ac1syQewExGw",
		"C2zfwTM9uWuMUA3zssbXRHgPJhKpUeWBd1"
	],
	"block_hash": "00009caa24b8f57ad9a94a917d2cc82e84afca84934cae7d7c2a5fba147e477f",
	"block_height": 174429,
	"block_index": 1,
	"confidence": 1,
	"confirmations": 2838,
	"confirmed": "Fri, 25 Feb 2022 04:25:18 GMT",
	"double_spend": false,
	"fees": 18200,
	"hash": "1e4fc540891e7e74127405b2b60a75f64b1e96724528226ecb2b85a828fa2842",
	"inputs": [{
		"addresses": [
			"C2zfwTM9uWuMUA3zssbXRHgPJhKpUeWBd1"
		],
		"age": 174428,
		"output_index": 1,
		"output_value": 99451600,
		"prev_hash": "d39ac0417e7d3ff01c426d70391dd4e1225563e8c20f2a91fc135837d9b9474b",
		"script": "47304402203300d1493ee1b1700a99b8ebb9386d8848a8620f47bf155e76b3739a4162f93a02206cc13d01d0ee72d92199440043d64b39254051bb559dfde0515cab526233c6830121038d3282aa146e680939aaa7896d68614994867e7b1c37672674c8cb47ba33b671",
		"script_type": "pay-to-pubkey-hash",
		"sequence": 4294967295
	}],
	"outputs": [{
			"addresses": [
				"BsCBSiUzqnTQgnHrSejfg5ac1syQewExGw"
			],
			"script": "76a91400bc897b9be08f14ac0584e5ba81410a1b9d90fb88ac",
			"script_type": "pay-to-pubkey-hash",
			"value": 500000
		},
		{
			"addresses": [
				"C2zfwTM9uWuMUA3zssbXRHgPJhKpUeWBd1"
			],
			"script": "76a9146c4097165af871b2f739aee04a9dd83df9292b5d88ac",
			"script_type": "pay-to-pubkey-hash",
			"spent_by": "be2a2d708c0ddebf6638f0f093d960216e8cdd6595d3764a75e16777bd1442da",
			"value": 98933400
		}
	],
	"preference": "medium",
	"received": "Fri, 25 Feb 2022 04:24:52 GMT",
	"relayed_by": "108.5.10.99",
	"size": 225,
	"total": 99433400,
	"ver": 1,
	"vin_sz": 1,
	"vout_sz": 2,
	"vsize": 225
}
```