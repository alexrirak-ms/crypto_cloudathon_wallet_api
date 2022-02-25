SELECT private_key from wallet
inner join crypto_connection_details ccd on wallet.connection_id = ccd.connection_id
where wallet_id = '%s'