import tarantool

# Query parameters
query = {
            "join": {
                "accounts": { # space
                    "acc_type": { # [filter]
                        "eq": ":account_type" # equals operation
                    }
                },
                "cards": { # space
                    "status": ":card_status"
                },
                "on": ["acc_id", "account_id"]
            },
            "fields": { # [fields for selection]
                "acc_id", "acc_type", "accounts.amount.value", "accounts.amount.currency",
                "cards.card_number", "cards.expiry_date", "cards.status"
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
                "limit": 1 # [paging]
            }
        }

# request
result = tarantool.api.find(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": [
        {
            "acc_id": "00012345678",
            "acc_type": "saving",
            "amount": {
                value": "1000",
                "currency": "840"
            }
        }
    }]
}
"""
opts = {
            "options": {
                "format": {
                    "flatten": "false",
                    "pretty": "true"
                },
                "after": result['result'][0] # [paging]
                "limit": 1
            }
        }
result = tarantool.api.find(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": [
        {
        "acc_id": "99912345678",
        "acc_type": "saving",
        "amount": {
            value": "50000",
            "currency": "643"
        },
        "card_number": "1111222233334444",
        "expiry_date": "1122",
        "status": "active",
    }]
}
"""
