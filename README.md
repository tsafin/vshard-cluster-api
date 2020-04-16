# vshard cluster api

## CRUD operations
### Select
`vshard.find` - search for records from a space, that fit conditions
```python
result, err = vshard.find(
    space="accounts",
    conditions=[('acc_type', '=', ':account_type'), ('amount', '>', 0)],
    params={"account_type": "saving"},
    opts = {"limit": 2}) # [paging]
"""
sample response
[("00012345678", "saving", {"1000", "840"}),
("99912345678", "saving", {"50000", "643"})]
"""
```

`vshard.get` - search for a record (like `find` with parameter `"limit" = 1`).
Returns only one record (if any).
```python
result, err = vshard.get(
    space="accounts",
    conditions=[('acc_id', '=', '99912345678')])
"""
sample response
("99912345678", "saving", {"1000", "840"})
"""
```

### Insert
`vshard.insert` - insert tuple into space
```python
result, err = vshard.insert(
    query="accounts",
    params=[("99912345678", "saving", "50000")])
```

`vshard.batch.insert` - insert array of tuples using batching
```python
result, err = vshard.batch.insert(
    space="accounts",
    params=[("00012345678", "saving", "1000"), ("99912345678", "saving", "50000", "840")],
    opts = {"batch_size": 20})
```

### Update
`vshard.update` - update tuple in space
```python
result, err = vshard.update(
    space="accounts"
    conditions=[('acc_id', '=', '?')],
    mutations=[('amount', '+', '?')],
    params=[("99912345678", 20000)],
    opts = {"cas_cond": "amount = 30000"}) # [optimistic lock]
```

`vshard.batch.update` - update array of tuples using batching
```python
result, err = vshard.batch.update(
    space="accounts",
    conditions=[('acc_id', '=', '?')],
    mutations=[('amount', '+', '?')],
    params=[("99912345678", 20000),("00012345678", 1000)],
    opts = {"batch_size": 20})
```

### Delete
`vshard.delete` - delete tuples from space
```python
result, err = vshard.delete(
    space="accounts",
    conditions=[('acc_id', '=', '99912345678')])
```

## Joins
`vshard.join` - joins 2 or more spaces, return aggregated result from all nodes.
```python
result, err = vshard.join(
    spaces=["accounts", "cards"],
    conditions=[('accounts.acc_id', '=', 'cards.account_id'), \
        ('accounts.account_type', '=', 'saving')],
    fields={'acc_id', 'acc_type', 'amount', \
            'cardnumber', 'expire_date', 'cards.status'})
"""
[("00012345678", "saving", "1000", "1111222233334444", "1122", "active")]
"""
```

## Functions
### Register function
`vshard.register` - register custom function in cluster. 
Returns hash code for function, it should be used to call registered function.
```python
result, err = vshard.register("local user = ...\n return 'Hello ' .. user")
"""
86c0f50124ea8abaf6624794b74c5654587a8f72
"""
```

### Call function
`vshard.register` - register custom function in cluster. 
Returns hash code for function, it should be used to call registered function.
```python
# call on all nodes registered function
result, err = vshard.call(func_hash, params)
# call on all nodes plain script
result, err = vshard.call(
    "local user = ...\n return 'Hello ' .. user", params)
# call by sharding key
result, err = vshard.call("accounts", ('acc_id', '=', '99912345678'), func_hash, params)
```

## Map/Reduce
`vshard.join` - joins 2 or more spaces, return aggregated result from all nodes.
```python
# map_func - <hash code of registered function or plain text
# reduce_func - <hash code of registered function or plain text
result, err = vshard.map_reduce(
    space="accounts",
    conditions=[('acc_type', '=', 'cash')],
    opts = {
        "map": map_func,
        "reduce": reduce_func,
        # or
        "map_hash": map_func_hash,
        "reduce_hash": reduce_func_hash
    })
"""
[]
"""
```

## Transactions