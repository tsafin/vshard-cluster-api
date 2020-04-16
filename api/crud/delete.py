
result, err = vshard.delete(
    space="accounts",
    conditions=[('acc_id', '=', '99912345678')])
# or
query = vshard.query(
    query="DELETE FROM accounts AS a WHERE a.acc_id = ?",
    params={"99912345678"},
    opts = {})
result, err = query.execute()
"""
[]
"""