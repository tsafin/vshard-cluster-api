import tarantool

# Query parameters
query = {
            "accounts": { # space
                "acc_id": ":account_id" # [filter]
            },
            "fields": { # [fields for selection]
                "acc_id", "acc_type", "amount.value", "amount.currency"
            }
        }
params = {
            "account_id": "99912345678"
        }
opts = {
            "options": {
                "format": {
                    "flatten": "false",
                    "pretty": "true"
                }
            }
        }

# request
result = tarantool.api.get(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "acc_id": "99912345678",
        "acc_type": "saving",
        "amount": {
          value": "1000",
          "currency": "840"
        }
    }
}
"""