# Cache

Функционал динамического создания key-value кешей. 

`vshard.cache_put` - запись значения в кеш. Если кеш не существует, он будет создан автоматически.

Формат запроса:
```lua
local result, err = vshard.cache_put(cache, key, value, opts) 
```

* `cache` - имя кеша
* `key` - ключ в кеше. Если значение с таким ключом в кеше есть, то значение будет перезаписано.
* `value` - значение
* `opts` - дополнительные опции запроса:
  * `timeout` - время ожидания записи (по-умолчанию 10000 мс).
  * `ttl` - время жизни записи в кеше (в мс, по-умолчанию не ограничено). 
  Если задано, то по истечению времени запись с ключом `key` будет удалена.
* `result` - nil
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
local result, err = vshard.cache_put("counters", "customer_1", { name = "John", amount = 20 })
```
---
`vshard.cache_get` - чтение значения из кеша по ключу. 

Формат запроса:
```lua
local result, err = vshard.cache_get(cache, key, opts) 
```

* `cache` - имя кеша
* `key` - ключ в кеше. 
* `opts` - дополнительные опции запроса:
  * `timeout` - время ожидания чтения (по-умолчанию 10000 мс).
* `result` - значение, соответствующее ключу `key`, или `nil`, если в кеше ключ не был найден.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
data, err = vshard.cache_get("counters", "customer_1") 
```
---
`vshard.cache_find` - чтение по ключу части значения по JSONPath. 

Формат запроса:
```lua
local result, err = vshard.cache_find(cache, key, path, opts) 
```

* `cache` - имя кеша
* `key` - ключ в кеше. 
* `path` - JSONPath для поиска значения (по-умолчанию `$[*]`). 
* `opts` - дополнительные опции запроса:
  * `timeout` - время ожидания чтения (по-умолчанию 10000 мс).
* `result` - значение, соответствующее ключу `key`, или `nil`, если в кеше ключ не был найден.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
local result, err = vshard.cache_find("counters", "customer_1", "$[*].name")
--[[ sample result
{ "John" }
]]--
```
---
`vshard.cache_invalidate` - удаление всех данных из кеша. 

Формат запроса:
```lua
local result, err = vshard.cache_invalidate(cache) 
```

* `cache` - имя кеша
* `result` - `nil`.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
local result, err = vshard.cache_invalidate("counters")
```
