
result, err = vshard.find(
    space="accounts",
    condition="acc_type = :account_type and amount > 0",
    params={"account_type": "saving"},
    opts = {"limit": 2}) # [paging]
"""
sample response
[("00012345678", "saving", {"1000", "840"}),
("99912345678", "saving", {"50000", "643"})]
"""
