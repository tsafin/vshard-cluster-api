import tarantool

# Query parameters
query = {
            "accounts": { # space
                "acc_id": ":account_id", # [fields]
                "acc_type": ":acc_type",
                "amount.value": ":amount_value",
                "amount.curr": ":amount_curr" # field with default value
            }
        }
params = [{
            "account_id": "00012345678",
            "acc_type": "saving",
            "amount_value": "1000"
        },
        {
            "account_id": "99912345678",
            "acc_type": "saving",
            "amount_value": "50000",
            "amount_curr": "643",
        }]
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
result = tarantool.api.insertBatch(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "insert": {
            "success": 2,
            "fail": 0
        }
    }
}
"""