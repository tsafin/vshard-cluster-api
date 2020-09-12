### Pub/Sub
Message exchange between publishers and subscribers.

---
`vshard.channel_publish` - запись сообщения в канал `channel`. Если канал не существует, он будет создан.

Формат запроса:
```lua
local result, err = vshard.channel_publish(channel, message) 
```

* `channel` - имя канала
* `message` - сообщения для передачи через канал 
* `opts` - дополнительные опции запроса:
  * `timeout` - время записи сообщения в канал (по-умолчанию 10000 мс). 
* `result` - `nil`
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
vshard.channel_publish("user messages", "some message")
```
---
`vshard.channel_subscribe` - подписка на сообщение из канала.

Формат запроса:
```lua
local result, err = vshard.channel_subscribe(channel, handler, opts) 
```

* `channel` - имя канала
* `handler` - функция обработки сообщений из канала
* `opts` - дополнительные опции запроса:
  * `timeout` - время чтения сообщения из канала (по-умолчанию 10000 мс). 
  * `offset` - номер смещения, после которого надо прочитать следующее сообщение из канала.
  * `filter` - фильтр входящих сообщений.
* `result` - кортеж в формате `{message_body, message_offset}`, где `message_body` - тело сообщения, 
`message_offset` - смещение текущего сообщения в канале.
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
local function handler(message) 
    -- process message  
end
local result, err = vshard.subscribe("user messages", handler, 
    { filter = {'=', 'acc_type', 'saving'}}) --opts
```
---
`vshard.unsubscribe` - отмена подписки на канал.

Формат запроса:
```lua
local result, err = vshard.unsubscribe(channel) 
```

* `channel` - имя канала
* `result` - `nil`
* `err` - код ошибки, если при выполнении запроса произошла исключительная ситуация
  
Пример:
```lua
-- unsubscribe from a channel
local result, err = vshard.unsubscribe(channel_name)
```
---
