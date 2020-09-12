## Map/Reduce
`vshard.map_reduce` - выполнение map/reduce над данными из спейса

Формат запроса:
```lua
local result, err = vshard.map_reduce(space, conditions, params, opts) 
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
  * `balance` - boolean флаг, задающий разрешение на чтение с реплик (по-умолчанию, true). 
* `result` - массив найденных кортежей
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
-- map_func_hash - hash code of registered function 
-- reduce_func_hash - hash code of registered function 
local result, err = vshard.map_reduce("accounts",
    {{'=', 'acc_type', '?'}}, -- conditions
    {'cash'}, -- params
    { -- opts
        map_hash = map_func_hash,
        reduce_hash = reduce_func_hash
    })
```
