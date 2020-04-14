
# create or get queue configuration
queue, err = vshard.queue(
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
err = queue.put(("some", "data"), ttl=2000)

# blocking push message to the queue with timeout
err = queue.offer(("some", "data"), timeout=5000)

# read and remove message from the queue
# if queue is empty, return empty null
data, err = queue.take()

# read and remove message from the queue,
# operation blocks until message is received or read_timeout
data, err = queue.poll(timeout=5000)

# peek - read and do not remove message.
# option to lock message for reads by other clients
# if queue is empty return null
data, err = queue.peek(lock=true)

# remove - remove locked message
data, err = queue.remove(data)
