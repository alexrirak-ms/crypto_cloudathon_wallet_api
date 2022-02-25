SELECT wallet_id, user_id, sc.chain_id, sc.name, sc.symbol, ccd.public_address, ccd.public_key from wallet
inner join crypto_connection_details ccd on wallet.connection_id = ccd.connection_id
inner join supported_chains sc on ccd.chain_id = sc.chain_id
where user_id = '%s'