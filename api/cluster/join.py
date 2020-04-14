import tarantool

result, err = vshard.join(
    spaces={"accounts", "cards"},
    condition="accounts.acc_id = cards.account_id \
        and accounts.account_type = ?"
    params={"saving"},
    opts = {})
# or
query = vshard.query(
    query="""FROM accounts AS a
             JOIN cards as c ON a.acc_id = c.account_id
             WHERE a.acc_type = :account_type""",
    params={"account_type": "saving"},
    opts = {})
result, err = query.execute()
"""
sample response
[("00012345678", "saving", "1000", "1111222233334444", "1122", "active")]
"""
