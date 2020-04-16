
result, err = vshard.join(
    spaces=["accounts", "cards"],
    conditions=[('accounts.acc_id', '=', 'cards.account_id'), \
        ('accounts.account_type', '=', 'saving')],
    fields={'acc_id', 'acc_type', 'amount', \
            'cardnumber', 'expire_date', 'cards.status'})
"""
[("00012345678", "saving", "1000", "1111222233334444", "1122", "active")]
"""
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
