
# publish message to a existing or new channel
pub, err = vshard.publish(
    channel="user messages"
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

def handler(message):
    print(message)
# subscribe to a channel, specify handler for incoming messages
sub, err = vshard.subscribe(channel="user messages", handler)

# unsubscribe from a channel
err = vshard.unsubscribe(channel="user messages")
