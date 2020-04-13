import tarantool

# Query parameters
query = [{
            "accounts": { # space
                "acc_id": ":account_id", # [fields]
                "acc_type": ":acc_type",
                "amount.value": ":amount_value",
                "amount.curr": ":amount_curr" # field with default value
            }
        },
        {
            "accounts": { # space
                "acc_id": ":account_id", # [fields]
                "acc_type": ":acc_type",
                "amount.value": ":amount_value",
                "amount.curr": ":amount_curr" # field with default value
            }
        },
        {
            "accounts": { # space
                "acc_id": ":account_id", # [filter]
            },
            "set": { # set of new values
                "acc_type": ":acc_type"
            }
        },
        {
            "accounts": { # space
                "acc_id": ":account_id" # [filter]
            }
        }
        ]
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
        },
        {
            "account_id": "99912345678",
            "acc_type": "checking"
        },
        {
            "account_id": "99912345678"
        }]
opts = {
            "options": {
                "format": {
                    "flatten": "false",
                    "pretty": "true"
                },
                "transaction_keys": ["99912345678"] # for optimistic locking
                "bucket_key": ["acc_type", "amount.curr"] # to get bucket_id
            }
        }

# request
result = tarantool.api.bulk(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "insert": {
            "success": 2,
            "fail": 0
        },
        "update": {
            "success": 1,
            "fail": 0
        },
        "delete": {
            "success": 0,
            "fail": 1
        }
    }
}
"""