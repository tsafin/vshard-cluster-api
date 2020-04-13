import tarantool

# Query parameters
query = {
            "accounts": { # space
                "acc_id": ":account_id" # [filter]
            }
        }
params = {
            "account_id": "99912345678"
        }
opts = {}

# request
result = tarantool.api.delete(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "delete": {
            "success": 1,
            "fail": 0
        }
    }
}
"""