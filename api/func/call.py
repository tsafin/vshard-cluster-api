
# call on all nodes registered function
result, err = vshard.call(func_hash, params)
# call on all nodes script
result, err = vshard.call(
    "local user = ...\n return 'Hello ' .. user", params)
# call by sharding_key
result, err = vshard.call("accounts", "acc_id=123", func_hash, params)