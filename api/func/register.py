import tarantool

# Query parameters
query = {
            "function": {
                "name": ":name"
                "data": ":file_path"
            }
        }
params = [{
            "name": "custom_script"
            "file": "script.lua"
        },
        {
            "name": "custom_expression"
            "expression": "local user = ...\n return 'Hello ' .. user"
        }]
opts = {
            "options": {
                "bucket_id": 228 # [bucket_id]
            }
        }

# request
result = tarantool.api.register(query, params, opts)
"""
sample response
{
    "status": "200",
    "result": {
        "register": {
            "success": 2,
            "fail": 0
        }
    }
}
"""
