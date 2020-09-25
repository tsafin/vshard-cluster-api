# Transactions

## Deadlock-free transaction
Обновление данных при помощи оптимистичных блокировок. В качестве поля для сравнения изменений в операции из `cas_cond`
должно быть поле целочисленного типа, которое будет увеличено на 1, если проверка `cas_cond` выполнима на момент 
применения изменений.
  
Пример:
```lua
local result, err = vshard.update("accounts",
    {{'=', 'acc_id', '99912345678'}}, --conditions
    {{'+', 'amount', '20000'}}, -- operations
    { cas_cond = {'=', 'version', '1'}}) -- opts
```
---

## Distributed transaction
`vshard.tx_begin` - создание контекста транзакции.
Формат запроса:
```lua
local result, err = vshard.tx_begin() 
```

* `result` - идекнтификатор транзакции
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация

---
`vshard.tx_commit` - создание контекста транзакции.
Формат запроса:
```lua
local result, err = vshard.tx_commit(transaction_id) 
```

* `transaction_id` - идентификатор транзакции, к которой применяется commit. Все изменения этой транзакции
будут применены на всех участвующих в транзакции узлах.
* `result` - `nil`
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация

Пример:
```lua
local tx_id = vshard.tx_begin()
-- specify transaction id in parameter `tx_id` for interactive transaction
local result, err = vshard.get("accounts", '99912345678', tx_id)
if result ~= nil then
    local result, err = vshard.insert("accounts", {"99912345678", "saving", "50000"}, tx_id)
end
result, err = vshard.update("accounts",
    {{'+', 'amount', '20000'}},
    {{'=', 'acc_status', 'active'}},
    tx_id)
-- commit transaction 
result, err = vshard.tx_commit(tx_id)
```
