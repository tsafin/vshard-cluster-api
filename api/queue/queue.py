"""
 Queue
"""
# create or get queue configuration
err = vshard.create_queue(
    channel="system messages"
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "lock_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

# push message to the queue
# optional ttl - time to live for the message.
# it should not be read once ttl's passed
err = vshard.put(("some", "data"), ttl=2000)

# blocking push message to the queue with timeout
err = vshard.offer(("some", "data"), timeout=5000)

# read and remove message from the queue
# if queue is empty, return empty null
data, err = vshard.take()

# read and remove message from the queue,
# operation blocks until message is received or read_timeout
data, err = vshard.poll(timeout=5000)

# peek - read and do not remove message.
# option to lock message for reads by other clients
# if queue is empty return null
data, err = vshard.peek(lock=true)

# remove - remove locked message
data, err = vshard.remove(data)

"""
 Pub/Sub
"""
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

