
result, err = vshard.get(
    space="accounts",
    conditions=[('acc_id', '=', '99912345678')])
# or
query = vshard.query(
    query="FROM accounts AS a WHERE a.acc_id = ?",
    params=["99912345678"],
    opts = {})
result, err = query.execute()
"""
sample response
("99912345678", "saving", {"1000", "840"})
"""