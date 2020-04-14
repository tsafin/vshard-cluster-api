
result, err = vshard.find(
    space="accounts",
    condition="acc_type = :account_type and amount > 0",
    params={"account_type": "saving"},
    opts = {"limit": 2}) # [paging]
# or
stmt = vshard.prepare(
    query="FROM accounts AS a WHERE a.acc_type = :account_type",
    params={"account_type": "saving"},
    opts = {"limit": 2}) # [paging]
result, err = stmt.execute()
"""
sample response
[("00012345678", "saving", {"1000", "840"}),
("99912345678", "saving", {"50000", "643"})]
"""
stmt.opts = {"after": result[1], "limit": 1} # [paging]
result, err = stmt.execute()
"""
sample response
("4678213812", "checking", {"2000", "840"})
"""
