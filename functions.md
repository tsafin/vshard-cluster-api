## Functions
### Register function
`vshard.register` - регистрация пользовательской функции. 

Формат запроса:
```lua
local result, err = vshard.register(func) 
```

* `func` - lua скрипт для регистрации в кластере
* `result` - hash код зарегистрированной функции. Должен быть использован для вызова функции.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
local result, err = vshard.register("local user = ...\n return 'Hello ' .. user")
"""
86c0f50124ea8abaf6624794b74c5654587a8f72
"""
```
---
### Call function
`vshard.call` - вызов зарегистрированной функции. 

Формат запроса:
```lua
local result, err = vshard.call(func, params, space, key) 
```

* `func` - hash код зарегистрированной функции (см. [vshard.register](#register-function)).
* `params` - массив значений аргументов функции
* `space` - спейс для определения ключа шардирования
* `key` - ключ кортежа. Если задан вместе со `space`, функция будет выполнена только на узле, где хранится кортеж с данным ключом.
* `params` - массив значений аргументов функции
* `result` - hash код зарегистрированной функции. Должен быть использован для вызова функции.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
-- call on all nodes registered function
local result, err = vshard.call("86c0f50124ea8abaf6624794b74c5654587a8f72", {"world"})
-- call by sharding key
local result, err = vshard.call("86c0f50124ea8abaf6624794b74c5654587a8f72", {"world"}, 
    "accounts", "99912345678")
```
---
### Eval function
`vshard.eval` - выполнении lua фунции в кластере. 

Формат запроса:
```lua
local result, err = vshard.eval(func, params, space, key) 
```

* `func` - lua скрипт для выполнения.
* `params` - массив значений аргументов функции
* `space` - спейс для определения ключа шардирования
* `key` - ключ кортежа. Если задан вместе со `space`, функция будет выполнена только на узле, где хранится кортеж с данным ключом.
* `params` - массив значений аргументов функции
* `result` - hash код зарегистрированной функции. Должен быть использован для вызова функции.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
-- call on all nodes plain script
local result, err = vshard.eval("local user = ...\n return 'Hello ' .. user", {"world"})
-- call by sharding key
local result, err = vshard.eval("local user = ...\n return 'Hello ' .. user", {"world"}, 
    "accounts", "99912345678")
```
