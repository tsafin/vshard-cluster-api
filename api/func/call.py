import tarantool

# call on all nodes registered function
result, err = tarantool.call(func_hash, params)
# call on all nodes script
result, err = tarantool.call(
    "local user = ...\n return 'Hello ' .. user", params)
# call by sharding_key
result, err = tarantool.call("accounts", "acc_id=123", func_hash, params)