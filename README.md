# vshard cluster api

## CRUD operations
### Select
`vshard.select` - search for records from a space, that fit conditions
```python
result, err = vshard.select(
    space="accounts",
    conditions=[('acc_type', '=', 'saving'), ('amount', '>', 0)],
    opts = {"limit": 2}) # [paging]
"""
sample response
[("00012345678", "saving", {"1000", "840"}),
("99912345678", "saving", {"50000", "643"})]
"""
# select data for the next page
result, err = vshard.select(
    space="accounts",
    conditions=[('acc_type', '=', 'saving'), ('amount', '>', 0)],
    opts = {"after": result[1], "limit": 2}) # [paging]
"""
sample response
("4678213812", "checking", {"2000", "840"})
"""
```

`vshard.get` - search for a record (like `select` with parameter `"limit" = 1`).
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

`vshard.batch_insert` - insert array of tuples using batching
```python
result, err = vshard.batch_insert(
    space="accounts",
    params=[("00012345678", "saving", "1000"), ("99912345678", "saving", "50000", "840")],
    opts = {"batch_size": 20})
```

### Update
`vshard.update` - update tuple in space
```python
result, err = vshard.update(
    space="accounts"
    conditions=[('acc_id', '=', '99912345678')],
    mutations=[('amount', '+', '20000')]) 
```

`vshard.batch_update` - update array of tuples using batching
```python
result, err = vshard.batch_update(
    space="accounts",
    set=[('amount', '+', '?')],
    conditions=[('acc_id', '=', '?')],
    params=[("99912345678", 20000),("00012345678", 1000)],
    opts = {"batch_size": 20})
```

### Upsert
`vshard.upsert` - insert new or update existing tuple in space
```python
result, err = vshard.insert(
    query="accounts",
    conditions=[('acc_id', '=', '99912345678')],
    mutations=[('amount', '=', '20000'), ('acc_type', '=', 'new')]) 
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
    on=[('accounts.acc_id', '=', 'cards.account_id'), \
        ('accounts.account_type', '=', 'saving')],
    conditions=[('amount', '>', 0)]
    fields={'acc_id', 'acc_type', 'amount', \
            'cardnumber', 'expire_date', 'cards.status'},
    opts = {"explain": false}) # return execution plan for the join query
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
`vshard.map_reduce` - map/reduce operation on data from `space`
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

## Queues
### FIFO queue
`vshard.queue` - fifo queue with blocking and non-blocking operations.
```python
# create new queue if not exists
queue_name = "system messages"
err = vshard.queue.create(
    name=queue_name
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "lock_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

# push message to the queue
# optional ttl - time to live for the message.
# it should not be read once ttl's passed
err = vshard.queue.put(queue_name, ("some", "data"), ttl=2000)

# blocking push message to the queue with timeout
err = vshard.queue.offer(queue_name, ("some", "data"), timeout=5000)

# read and remove message from the queue
# if queue is empty, return empty null
data, err = vshard.queue.take(queue_name)

# read and remove message from the queue,
# operation blocks until message is received or read_timeout
data, err = vshard.queue.poll(queue_name, timeout=5000)

# peek - read and do not remove message.
# option to lock message for reads by other clients
# if queue is empty return null
data, err = vshard.queue.peek(queue_name, lock=true)

# remove - remove locked message
data, err = vshard.queue.remove(queue_name, data)

# delete - delete queue
err = vshard.queue.delete(queue_name)
```

### Pub/Sub
`vshard.channel` - message exchange between publishers and subscribers
```python
# create new channel
channel_name = "user messages"
err = vshard.channel.create(
    channel=channel_name
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

# publish message to an existing channel
vshard.channel.publish(channel_name, "some message")

def handler(messages):
    for m in messages: print(m)
# subscribe to a channel, specify handler for incoming messages
err = vshard.subscribe(channel_name, handler)

# unsubscribe from a channel
err = vshard.unsubscribe(channel_name)
```

## Transactions
Deadlock-free transaction
```python
# update with optimistic lock. field from cas_cond should be inc on succesfull update atomically.
result, err = vshard.update(
    space="accounts"
    conditions=[('acc_id', '=', '99912345678')],
    mutations=[('amount', '+', '20000')],
    opts = {"cas_cond": ('version', '=', '1')}) # [optimistic lock condition]
```
Execute different query statement in one transaction
```python
queries = [
    { op="insert", 
        query="accounts",
        params=[("99912345678", "saving", "50000")] },
    { op="update",
        space="accounts"
        conditions=[('acc_id', '=', '99912345678')],
        mutations=[('amount', '+', '20000')]) }]
result, err = vshard.tx_execute(queries)
```

## Explain plan
`explain` option - returns query execution plan.
```python
result, err = vshard.select(
    space="accounts",
    conditions=[('acc_id', '=', '99912345678')],
    opts = {"explain": true}) # explain plan of query execution
"""
# json-like tree with query plan
"""
```