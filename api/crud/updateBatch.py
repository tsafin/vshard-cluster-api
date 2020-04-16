
result, err = vshard.batch.update(
    space="accounts",
    conditions=[('acc_id', '=', '?')],
    mutations=[('amount', '+', '?')],
    params=[("99912345678", 20000),("00012345678", 1000)],
    opts = {"batch_size": 20})
# or
# sharding key registration is out of scope
result, err = vshard.prepareBatch(
    query="INSERT ? INTO accounts",
    params={("00012345678", "saving", "1000"), ("99912345678", "saving", "50000", "840")})
# or
query = vshard.prepareBatch(query="INSERT ? INTO accounts")
query.addBatch(("00012345678", "saving", "1000"))
query.addBatch(("99912345678", "saving", "50000"))

result, err = query.executeBatch()
"""
[("00012345678", "saving", "1000"), ("99912345678", "saving", "50000", "840")]
"""