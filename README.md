# vshard cluster api

## CRUD operations
### Select
`vshard.select` - search for records from a space, that fit conditions
```python
result, err = vshard.select(
    space="accounts",
    conditions=[('=', 'acc_type', 'saving'), ('>', 'amount', 0)],
    opts = {"limit": 2}) # [paging]
"""
sample response
[("00012345678", "saving", {"1000", "840"}),
("99912345678", "saving", {"50000", "643"})]
"""
# select data for the next page
result, err = vshard.select(
    space="accounts",
    conditions=[('=', 'acc_type', 'saving'), ('amount', '>', 0)],
    opts = {"after": result[1], "limit": 2}) # [paging]
"""
sample response
("4678213812", "checking", {"2000", "840"})
"""
```

`vshard.get` - search for a record (like `select` with parameter `"limit" = 1`).
Returns only one record (if any).
```python
result, err = vshard.get(space="accounts", key='99912345678')
"""
sample response
("99912345678", "saving", {"1000", "840"})
"""
```

### Insert
`vshard.insert` - insert tuple into space
```python
result, err = vshard.insert(space="accounts", tuple=("99912345678", "saving", "50000"))
```

`vshard.batch_insert` - insert array of tuples using batching
```python
result, err = vshard.batch_insert(
    space="accounts",
    tuples=[("99912345678", "saving", "50000"),("99912345678", "saving", {"50000", "643"})],
    opts = {"batch_size": 20})
```

### Put
`vshard.put` - insert or replace tuple into space
```python
result, err = vshard.put(
    space="accounts",
    tuple=("00012345678", "saving", "1000"))
```

`vshard.put_all` - put array of tuples using batching
```python
result, err = vshard.put_all(
    space="accounts",
    tuples=[("99912345678", "saving", "50000"),("99912345678", "saving", {"50000", "643"})],
    opts = {"batch_size": 20})
```

### Update
`vshard.update` - update tuple in space
```python
result, err = vshard.update(
    space="accounts"
    set=[('+', 'amount', '20000')]) 
    conditions=[('=', 'acc_id', '99912345678')],
```

`vshard.batch_update` - update array of tuples using batching
```python
result, err = vshard.batch_update(
    space="accounts",
    set=[('+', 'amount', '?')],
    conditions=[('=', 'acc_id', '?')],
    params=[("99912345678", 20000),("00012345678", 1000)],
    opts = {"batch_size": 20})
```

### Upsert
`vshard.upsert` - insert new or update existing tuple in space
```python
result, err = vshard.upsert(
    space="accounts",
    set=[('=', 'amount', '20000'), ('=', 'acc_type', 'new')]) 
    tuple=("99912345678", "saving", "50000"),
```

`vshard.batch_upsert` - upsert array of tuples using batching
```python
result, err = vshard.batch_upsert(
    space="accounts",
    set=[('+', 'amount', '5000')],
    tuples=[("99912345678", "saving", "50000"),("99912345678", "saving", {"50000", "643"})],
    opts = {"batch_size": 20})
```

### Delete
`vshard.delete` - delete tuples from space
```python
result, err = vshard.delete(
    space="accounts",
    conditions=[('=', 'acc_type', 'saving')])
```

## Joins
`vshard.join` - joins 2 or more spaces, return aggregated result from all nodes.
```python
result, err = vshard.join(
    spaces=["accounts", "cards"],
    on=[('=', 'accounts.acc_id', 'cards.account_id'), \
        ('=', 'accounts.account_type', 'saving')],
    conditions=[('>', 'amount', 0)]
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
result, err = vshard.call("accounts", ('=', 'acc_id', '99912345678'), func_hash, params)
```

## Map/Reduce
`vshard.map_reduce` - map/reduce operation on data from `space`
```python
# map_func - <hash code of registered function or plain text
# reduce_func - <hash code of registered function or plain text
result, err = vshard.map_reduce(
    space="accounts",
    conditions=[('=', 'acc_type', 'cash')],
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

## Messaging
### FIFO queue
`vshard.queue` - queue with blocking and non-blocking operations. fifo is guaranteed on partition level.
```python
# create new queue if not exists
queue_name = "system messages"
err = vshard.queue_create(
    name=queue_name
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "lock_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

# push message to the queue
# ttl - time to live for the message.
# timeout - custom timeout for put operation
# partition - put message into specified queue partition
# it should not be read once ttl's passed
data, err = vshard.queue_put(queue_name, message=("some", "data"), partition=partition_id, ttl=2000, timeout=5000)

# read and remove message from the queue
# if queue is empty, return empty null
# timeout - custom timeout for take operation
# partition - get message from a specified queue partition
data, err = vshard.queue_take(queue_name, partition=partition_id, timeout=5000)

# peek - read and do not remove message. if queue is empty return null
# partition - peek message from a specified queue partition
# timeout - custom timeout for peek operation
# lock - option to lock message for reads by other clients
# lock_timeout - timeout after which lock will be invalidated
# returns tuples (message, lock_key). lock_key should be used to remove message from queue.
data, err = vshard.queue_peek(queue_name, partition=partition_id, timeout=5000, lock=true, lock_timeout=10000)

# remove - remove locked message
data, err = vshard.queue_remove(queue_name, data.lock_key, timeout=5000)

# delete - delete queue
err = vshard.queue_delete(queue_name)
```

### Pub/Sub
`vshard.channel` - message exchange between publishers and subscribers
```python
# create new channel
channel_name = "user messages"
err = vshard.channel_create(
    channel=channel_name
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

# publish message to an existing channel
vshard.channel_publish(channel_name, "some message")

def handler(messages):
    # each message is a tuple (message_body, message_offset)
    for m in messages: print(m)

# subscribe to a channel, specify handler for incoming messages
# filter - optional attribute to specify subscriber's message filter
# offset - message offset from which subscriber wants to consume 
err = vshard.subscribe(channel_name, handler, 
    opts = {"offset": message_offset,
            "filter": ('=', 'acc_type', 'saving')})

# unsubscribe from a channel
err = vshard.unsubscribe(channel_name)
```

## Transactions
### Deadlock-free transaction
```python
# update with optimistic lock. field from cas_cond should be inc on succesfull update atomically.
result, err = vshard.update(
    space="accounts"
    conditions=[('=', 'acc_id', '99912345678')],
    mutations=[('+', 'amount', '20000')],
    opts = {"cas_cond": ('=', 'version', '1')}) # [optimistic lock condition]
```

### Distributed transaction
```python
queries = [
    { op="insert", 
        space="accounts",
        params=[("99912345678", "saving", "50000")] },
    { op="update",
        space="accounts"
        conditions=[('=', 'acc_id', '99912345678')],
        mutations=[('+', 'amount', '20000')]) }]
# prepare transaction for execution on dedicated storages
tx_id, err = vshard.tx_prepare(queries)
# commit transaction 
result, err = vshard.tx_commit(tx_id)
```

## Explain plan
`explain` option - returns query execution plan.
```python
result, err = vshard.select(
    space="accounts",
    conditions=[('=', 'acc_id', '99912345678')],
    opts = {"explain": true}) # explain plan of query execution
"""
# json-like tree with query plan
"""
```