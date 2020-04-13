import tarantool

# Query parameters
query = {
            "accounts": { # space
                "acc_type": { # [filter]
                    "eq": ":account_type" # equals operation
                }
            },
            "fields": { # [fields for selection]
                "acc_id", "acc_type", "amount.value", "amount.currency"
            }
        }
params = {
            "account_type": "saving"
        }
opts = {
            "options": {
                "format": { # [response data format]
                    "flatten": "false",
                    "pretty": "true"
                },
                "bucket_id": [228] # to listen on specific nodes
            }
        }

def handler(data):
    print(data)

# request
socket = tarantool.api.listen(query, params, opts, handler)
