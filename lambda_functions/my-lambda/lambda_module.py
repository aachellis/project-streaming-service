import json

def handler(event, context):
    return {
        "status-code": 200,
        "body": json.dumps({
            "greetings": "Hello World"
        })
    }