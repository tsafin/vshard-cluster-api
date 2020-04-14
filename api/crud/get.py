
result, err = vshard.get(
    query="accounts",
    query="acc_id = ?",
    params={"99912345678"},
    opts = {})
# or
query = vshard.query(
    query="FROM accounts AS a WHERE a.acc_id = ?",
    params={"99912345678"},
    opts = {})
result, err = query.execute()
"""
sample response
("99912345678", "saving", {"1000", "840"})
"""