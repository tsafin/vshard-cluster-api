import tarantool

# Query parameters
query = {
            "function": {
                "name": ":name"
                "parameters": {
                    "param": ":param"
                }
            }
        }
params = {
            "name": "custom_expression"
            "param": "world"
        }
opts = {
            "options": {
                "bucket_id": 228 # [bucket_id]
            }
        }

# request
result = tarantool.api.call(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "Hello world"
    }
}
"""
