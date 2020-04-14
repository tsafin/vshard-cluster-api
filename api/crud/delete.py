
result, err = vshard.delete(
    space="accounts",
    condition="acc_id = ?",
    params={"99912345678"},
    opts = {})
# or
query = vshard.query(
    query="DELETE FROM accounts AS a WHERE a.acc_id = ?",
    params={"99912345678"},
    opts = {})
result, err = query.execute()
"""
[]
"""