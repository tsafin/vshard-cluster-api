import tarantool

def handler(data):
    print(data) #box.session.push and routing to a client

query = vshard.query(
    query="FROM accounts AS a WHERE a.acc_type = :account_type",
    params={"account_type": "saving"},
    opts = {})
result, err = tarantool.api.listen(query, handler)
