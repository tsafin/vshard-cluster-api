
result, err = vshard.insert(
    space="accounts",
    params=[("99912345678", "saving", "50000")])
#or
stmt = vshard.query(
    query="INSERT ? INTO accounts",
    params={("99912345678", "saving", "50000")},
    opts = {})
result, err = stmt.execute()
"""
("99912345678", "saving", "50000")
"""