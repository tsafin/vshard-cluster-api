import tarantool

# Query parameters
query = {
            "accounts": { # space
                "acc_type": { # [filter]
                    "ne": ":account_type" # not equals operation
                }
            },
            "fields": { # [fields for selection]
                "acc_id", "acc_type", "amount.value", "amount.currency"
            }
        }
params = {
           "account_type": "cash",
           "map": "map_function", # registered before map_reduce call
           "reduce": "reduce_function" # registered before map_reduce call
       }
opts = {
            "options": {
                "bucket_id": 228 # [bucket_id]
            }
        }

# request
result = tarantool.api.map_reduce(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        []
    }
}
"""
