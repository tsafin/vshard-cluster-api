
#map_func - <hash code of registered function or plain text
#reduce_func - <hash code of registered function or plain text
result, err = vshard.map_reduce(
    query="FROM accounts AS a WHERE a.acc_type <> :account_type",
    params={"account_type": "cash"},
    opts = {
        "map": map_func,
        "reduce": reduce_func,
        # or
        "map_hash": map_func_hash,
        "reduce_hash": reduce_func_hash
    })
"""
sample response
[]
"""
