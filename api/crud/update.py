import tarantool

# Query parameters
query = {
            "accounts": { # space
                "acc_id": ":account_id", # [filter]
            },
            "set": { # set of new values
                "acc_type": ":acc_type"
            }
        }
params = {
    "account_id": "99912345678",
    "acc_type": "checking"
}
opts = {}

# request
result = tarantool.api.update(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "update": {
            "success": 1,
            "fail": 0
        }
    }
}
"""