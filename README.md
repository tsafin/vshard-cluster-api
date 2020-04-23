# vshard cluster api

## CRUD operations
### Select
`vshard.select` - поиск данных в спейсе по набору условий. Если среди условий фильтрации есть сравнение поля 
шардирования с его полным значением, то запрос будет выполнен на узле, хранящем бакет этого ключа. Иначе запрос 
будет выполнен на всех узлах кластера, и для формирования результата неявно выполнен map-reduce результатов.

Формат запроса:
```lua
result, err = vshard.select(space, conditions, opts) 
```

* `space` - имя спейса
* `conditions` - массив условий фильтрации спейса в формате {operator, field_name, value} (см. [документацию](https://www.tarantool.io/en/doc/1.10/reference/reference_lua/box_space/#box-space-update))
* `opts` - дополнительные опции запроса:
  * `limit` - максимальное число кортежей в результате 
  * `after` - кортеж, после которого должны быть выбраны следующие за ним кортежи.
* `result` - массив кортежей, удовлетворяющие условиям запроса
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.select("accounts", {{'=', 'acc_type', 'saving'}, {'>', 'amount', 0}}, {limit = 2}) 
--[[ sample response
{{"00012345678", "saving", {"1000", "840"}},
{"99912345678", "saving", {"50000", "643"}}}
]]--
-- select data for the next page
result, err = vshard.select("accounts", {{'=', 'acc_type', 'saving'}, {'>', 'amount', 0}}, 
    {limit = 2, after = result[1]}) 
--[[ sample response
{{"4678213812", "checking", {"2000", "840"}}}
]]--
```
---
`vshard.get` - поиск кортежа по ключу.

Формат запроса:
```lua
result, err = vshard.get(space, key) 
```

* `space` - имя спейса
* `key` - значение индексного ключа
* `result` - кортеж, найденный в спейсе по ключу `key` или `nil`
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.get("accounts", '99912345678')
--[[ sample response
{"99912345678", "saving", {"1000", "840"}}
]]--
```
---
### Insert
`vshard.insert` - сохранение кортежа в спейсе.

Формат запроса:
```lua
result, err = vshard.insert(space, tuple) 
```

* `space` - имя спейса
* `tuple` - кортеж с данными
* `result` - кортеж, вставленный в спейс
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.insert("accounts", {"99912345678", "saving", "50000"})
--[[ sample response
{"99912345678", "saving", "50000"}
]]--
```
---
`vshard.batch_insert` - пакетное сохранение массива кортежей в спейсе.

Формат запроса:
```lua
result, err = vshard.batch_insert(space, tuples, opts) 
```

* `space` - имя спейса
* `tuples` - массив кортежей для сохранения
* `opts` - дополнительные опции запроса:
  * `batch_size` - число кортежей в одном батче
* `result` - массив кортежей, сохраненных в спейсе в последнем выполненном батче
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.batch_insert("accounts",
    {{"99912345678", "saving", "50000"},{"99912345678", "saving", {"50000", "643"}}},
    {batch_size = 20})
```
---
### Put
`vshard.put` - вставка или замена существующего кортежа в спейсе.

Формат запроса:
```lua
result, err = vshard.put(space, tuples) 
```

* `space` - имя спейса
* `tuple` - кортеж с данными
* `result` - кортеж, обновленный или вставленный в спейс
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.put("accounts", {"00012345678", "saving", "1000"})
--[[ sample response
{"00012345678", "saving", "1000"}
]]--
```
---
`vshard.batch_put` - вставка новых и обновление существующих кортежей в спейсе.

Формат запроса:
```lua
result, err = vshard.batch_put(space, tuples, opts) 
```

* `space` - имя спейса
* `tuples` - массив кортежей для сохранения или замены
* `opts` - дополнительные опции запроса:
  * `batch_size` - число кортежей в одном батче
* `result` - массив кортежей, сохраненных/обновленных в спейсе
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.batch_put(accounts,
    {{"99912345678", "saving", "50000"},{"99912345678", "saving", {"50000", "643"}}},
    {batch_size = 20})
```
---
### Update
`vshard.update` - обновление кортежа в спейсе

Формат запроса:
```lua
result, err = vshard.update(space, key, operations) 
```

* `space` - имя спейса
* `key` - значение индексного ключа кортежа
* `operations` - массив операций изменения данных в кортеже
* `result` - кортеж, обновленный в спейсе
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.update("accounts", "99912345678", {{'+', 'amount', '20000'}})
--[[ sample response
{"99912345678", "saving", "70000"}
]]--
```
---
`vshard.batch_update` - пакетное обновление кортежей в спейсе.

Формат запроса:
```lua
result, err = vshard.batch_update(space, conditions, operations, params, opts) 
```

* `space` - имя спейса
* `conditions` - массив условий поиска кортежей для обновления
* `operations` - массив операций изменения данных в кортеже
* `params` - массив значений параметров для операций и условий
* `opts` - дополнительные опции запроса:
  * `batch_size` - число кортежей в одном батче
* `result` - массив кортежей, обновленных в последнем выполненном батче
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.batch_update("accounts",
    {{'=', 'acc_id', ':account_id'}}, -- conditions
    {{'+', 'amount', ':add_amount'}}, -- operations
    {{account_id = "99912345678", add_amount = 20000},{account_id = "00012345678", add_amount = 1000}}, -- params
    {batch_size = 20}) -- opts
```
---
### Upsert
`vshard.upsert` - вставка нового или обновление существующего кортежа в спейсе.

Формат запроса:
```lua
result, err = vshard.upsert(space, tuple, operations) 
```

* `space` - имя спейса
* `tuple` - кортед с данными
* `operations` - массив операций изменения данных в кортеже
* `result` - `nil`
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.upsert("accounts",
    {"99912345678", "saving", "50000"},
    {{'=', 'amount', '20000'}, {'=', 'acc_type', 'new'}})
```
---
`vshard.batch_upsert` - пакетное выполнение операции `upsert`.

Формат запроса:
```lua
result, err = vshard.batch_upsert(space, tuples, operations, params, opts) 
```

* `space` - имя спейса
* `tuples` - массив кортежей для вставки или обновления
* `operations` - массив массивов операций изменения в кортежах. К кортежу по индексу n (tuples[n]) будут применены операции operations[n].
* `params` - массив значений параметров для операций и условий
* `opts` - дополнительные опции запроса:
  * `batch_size` - число кортежей в одном батче
* `result` - массив кортежей, обновленных в последнем выполненном батче
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.batch_upsert("accounts",
    {{"99912345678", "saving", "50000"},{"00012345678", "saving", {"50000", "643"}}}, -- tuples
    {{{'+', 'amount', '5000'}}, {{'-', 'amount', '5000'}}}, -- params
    {batch_size = 20}) -- opts
```
---
### Delete
`vshard.delete` - удаление кортежа из спейса по первичному ключу.

Формат запроса:
```lua
result, err = vshard.delete(space, key) 
```

* `space` - имя спейса
* `key` - значение первичного ключа
* `result` - удаленный кортеж
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.delete("accounts", "00012345678")
--[[ sample response
{"00012345678", "saving", "1000"}
]]--
```
---
`vshard.batch_delete` - удаление кортежей из спейса условию.

Формат запроса:
```lua
result, err = vshard.batch_delete(space, conditions, params, opts) 
```

* `space` - имя спейса
* `conditions` - массив условий поиска кортежей для удаления
* `params` - массив значений параметров для условий поиска
* `opts` - дополнительные опции запроса:
  * `batch_size` - число кортежей в одном батче
* `result` - массив кортежей, удаленных в последнем выполненном батче
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.batch_delete("accounts", 
    {{'=', 'acc_type', 'saving'}}, -- conditions
    {}, -- params
    {batch_size = 20} -- opts
    )
--[[ sample response
{{"00012345678", "saving", {"1000", "840"}},
{"99912345678", "saving", {"50000", "643"}}}
]]--
```
---
## Joins
`vshard.join` - join запрос к двум или более спейсам.

Формат запроса:
```lua
result, err = vshard.join(spaces, on, conditions, fields, params, opts) 
```

* `spaces` - список спейсов запроса
* `on` - массив условий объединения спейсов по ключам в формате `{{space1.field1, space2.field2}, ...}`
* `conditions` - массив условий поиска кортежей 
* `fields` - массив полей в возвращаемых кортежах
* `params` - массив значений параметров для условий поиска
* `opts` - дополнительные опции запроса:
  * `limit` - максимальное число кортежей в результате 
* `result` - массив найденных кортежей
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.join({"accounts", "cards"}, -- spaces
    {{'accounts.acc_id', 'cards.account_id'}}, -- on
    {{'>', 'accounts.amount', 0}, {'=', 'accounts.account_type', 'saving'}}, -- consitions
    {'accounts.acc_id', 'accounts.acc_type', 'accounts.amount', -- fields
     'cards.cardnumber', 'cards.expire_date', 'cards.status'}) 
--[[ sample response 
[("00012345678", "saving", "1000", "1111222233334444", "1122", "active")]
]]--
```
---
## Functions
### Register function
`vshard.register` - регистрация пользовательской функции. 

Формат запроса:
```lua
result, err = vshard.register(func) 
```

* `func` - lua скрипт для регистрации в кластере
* `result` - hash код зарегистрированной функции. Должен быть использован для вызова функции.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
result, err = vshard.register("local user = ...\n return 'Hello ' .. user")
"""
86c0f50124ea8abaf6624794b74c5654587a8f72
"""
```
---
### Call function
`vshard.call` - вызов зарегистрированной функции. 

Формат запроса:
```lua
result, err = vshard.call(func, params, space, key) 
```

* `func` - hash код зарегистрированной функции (см. [vshard.register](#register-function)) или lua скрипт для выполнения.
* `params` - массив значений аргументов функции
* `space` - спейс для определения ключа шардирования
* `key` - ключ кортежа. Если задан вместе со `space`, функция будет выполнена только на узле, где хранится кортеж с данным ключом.
* `params` - массив значений аргументов функции
* `result` - hash код зарегистрированной функции. Должен быть использован для вызова функции.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
-- call on all nodes registered function
result, err = vshard.call("86c0f50124ea8abaf6624794b74c5654587a8f72", {"world"})
-- call on all nodes plain script
result, err = vshard.call("local user = ...\n return 'Hello ' .. user", {"world"})
-- call by sharding key
result, err = vshard.call("86c0f50124ea8abaf6624794b74c5654587a8f72", {"world"}, 
    "accounts", "99912345678")
```
---
# TBD
Далее перечислены методы API, которые еще находятся на стадии обсуждения.

## Map/Reduce
`vshard.map_reduce` - выполнение map/reduce над данными из спейса

Формат запроса:
```lua
result, err = vshard.call(space, conditions, opts) 
```

* `space` - имя спейса
* `conditions` - массив условий поиска кортежей 
* `params` - массив значений параметров для условий поиска
* `opts` - дополнительные опции запроса:
  * `map` - тело функции map. 
  Имеет более высокий приоритет над `map_hash` (т.е. если указаны обе опции, выполняться будет функция, 
  заданная в `map`)
  * `reduce` - тело функции reduce. 
  Имеет более высокий приоритет над `reduce_hash` (т.е. если указаны обе опции, выполняться будет функция, 
  заданная в `reduce`)
  * `map_hash` - hash код зарегистрированной функции map. 
  * `reduce_hash` - hash код зарегистрированной функции reduce. 
* `result` - массив найденных кортежей
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
-- map_func_hash - hash code of registered function 
-- reduce_func_hash - hash code of registered function 
result, err = vshard.map_reduce("accounts",
    {{'=', 'acc_type', '?'}}, -- conditions
    {'cash'}, -- params
    { -- opts
        map_hash = map_func_hash,
        reduce_hash = reduce_func_hash
    })
```
---
## Messaging
### FIFO queue
`vshard.queue_create` - Создание распределенной очереди с гарантией fifo на уровне партиций.

Формат запроса:
```lua
result, err = vshard.queue_create(name, opts) 
```

* `name` - имя очереди
* `opts` - дополнительные опции запроса:
  * `read_timeout` - время ожидания чтения из очереди (мс).
  * `write_timeout` - время ожидания записи в очередь (мс).
  * `lock_timeout` - время . 
  * `reduce_hash` - hash код зарегистрированной функции reduce. 
* `result` - массив найденных кортежей
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
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
```lua
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
```lua
# update with optimistic lock. field from cas_cond should be inc on succesfull update atomically.
result, err = vshard.update(
    space="accounts"
    conditions=[('=', 'acc_id', '99912345678')],
    operations=[('+', 'amount', '20000')],
    opts = {"cas_cond": ('=', 'version', '1')}) # [optimistic lock condition]
```

### Distributed transaction
```lua
tx_id = vshard.tx_begin()
# specify transaction id in parameter `tx_id` for interactive transaction
result, err = vshard.get(space="accounts", key='99912345678', tx_id=tx_id)
if not result then:
    result, err = vshard.insert(space="accounts", 
        tuple=("99912345678", "saving", "50000"),
        tx_id=tx_id)
result, err = vshard.update(
    space="accounts"
    operations=[('+', 'amount', '20000')],
    conditions=[('=', 'acc_status', 'active')],
    tx_id=tx_id)
# commit transaction 
result, err = vshard.tx_commit(tx_id)
```

## Explain plan
`explain` option - returns query execution plan.
```lua
result, err = vshard.select(
    space="accounts",
    conditions=[('=', 'acc_id', '99912345678')],
    opts = {"explain": true}) # explain plan of query execution
"""
# json-like tree with query plan
"""
```