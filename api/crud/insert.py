import tarantool

# Query parameters
query = {
            "accounts": { # space
                "acc_id": ":account_id", # [fields]
                "acc_type": ":acc_type",
                "amount.value": ":amount_value"
            }
        }
params = {
            "account_id": "99912345678",
            "acc_type": "saving",
            "amount_value": "50000"
        }
opts = {
            "options": {
                "format": {
                    "flatten": "false",
                    "pretty": "true"
                },
                "bucket_key": ["acc_type", "amount.curr"] # to get bucket_id
            }
        }

# request
result = tarantool.api.insert(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "insert": {
            "success": 1,
            "fail": 0
        }
    }
}
"""