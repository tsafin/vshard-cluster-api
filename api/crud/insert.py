result, err = vshard.insert(
    query="accounts",
    params={("99912345678", "saving", "50000")},
    opts = {})
#or
stmt = vshard.query(
    query="INSERT ? INTO accounts",
    params={("99912345678", "saving", "50000")},
    opts = {})
result, err = stmt.execute()
"""
("99912345678", "saving", "50000")
"""