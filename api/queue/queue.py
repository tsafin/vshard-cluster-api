"""
 Queue
"""
# create new queue if not exists
queue_name = "system messages"
err = vshard.queue.create(
    name=queue_name
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "lock_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

# push message to the queue
# optional ttl - time to live for the message.
# it should not be read once ttl's passed
err = vshard.queue.put(queue_name, ("some", "data"), ttl=2000)

# blocking push message to the queue with timeout
err = vshard.queue.offer(queue_name, ("some", "data"), timeout=5000)

# read and remove message from the queue
# if queue is empty, return empty null
data, err = vshard.queue.take(queue_name)

# read and remove message from the queue,
# operation blocks until message is received or read_timeout
data, err = vshard.queue.poll(queue_name, timeout=5000)

# peek - read and do not remove message.
# option to lock message for reads by other clients
# if queue is empty return null
data, err = vshard.queue.peek(queue_name, lock=true)

# remove - remove locked message
data, err = vshard.queue.remove(queue_name, data)

# delete - delete queue
err = vshard.queue.delete(queue_name)

"""
 Pub/Sub
"""
# create new channel
channel_name = "user messages"
err = vshard.channel.create(
    channel=channel_name
    opts = {
        "read_timeout": "10000", # default parameters
        "write_timeout": "10000",
        "size": "100000",
        "ttl": "100000"})

# publish message to an existing channel
vshard.channel.publish(channel_name, "some message")

def handler(messages):
    for m in messages: print(m)
# subscribe to a channel, specify handler for incoming messages
err = vshard.subscribe(channel_name, handler)

# unsubscribe from a channel
err = vshard.unsubscribe(channel_name)

