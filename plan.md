## Explain plan
Возврат плана выполнения запроса.

Пример:
```lua
local result, err = vshard.select("accounts",
    {{'=', 'acc_id', '99912345678'}},
    {explain = true}) 
--[[
    json-like tree with query plan
]]--
```