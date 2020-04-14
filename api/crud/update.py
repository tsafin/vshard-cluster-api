
result, err = vshard.update(
    space="accounts"
    condition="acc_id = ?",
    params={"99912345678"},
    mutations={("amount + 20000")},
    opts = {"cas_cond": "amount = 30000"}) # [optimistic lock]
# or
result, err = vshard.query(
    query="UPDATE accounts SET amount = amount + ? WHERE acc_id = '99912345678'",
    params={"20000"},
    opts = {"cas_cond": "amount = 30000"}) # [optimistic lock]
"""
("99912345678", "saving", "50000")
"""