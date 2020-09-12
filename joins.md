## Joins
`vshard.join` - join запрос к двум или более спейсам.

Формат запроса:
```lua
local result, err = vshard.join(spaces, on, conditions, fields, params, opts) 
```

* `spaces` - список спейсов запроса
* `on` - массив условий объединения спейсов по ключам в формате `{{space1.field1, space2.field2}, ...}`
* `conditions` - массив условий поиска кортежей 
* `fields` - массив полей в возвращаемых кортежах
* `params` - массив значений параметров для условий поиска
* `opts` - дополнительные опции запроса:
  * `limit` - максимальное число кортежей в результате 
  * `balance` - boolean флаг, задающий разрешение на чтение с реплик (по-умолчанию, true).
  * `explain` - boolean флаг. Если задан в true, то вместо результата запроса будет возвращен план запроса 
  (по-умолчанию, false).
* `result` - массив найденных кортежей
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
local result, err = vshard.join({"accounts", "cards"}, -- spaces
    {{'accounts.acc_id', 'cards.account_id'}}, -- on
    {{'>', 'accounts.amount', 0}, {'!=', 'accounts.account_type', 'saving'}}, -- consitions
    {'accounts.acc_id', 'accounts.acc_type', 'accounts.amount', -- fields
     'cards.cardnumber', 'cards.expire_date', 'cards.status'}) 
--[[ sample response 
[("00012345678", "saving", "1000", "1111222233334444", "1122", "active")]
]]--
```
