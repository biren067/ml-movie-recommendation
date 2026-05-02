import json
from layers.common.python.helper import greeting


def lambda_handler(event, context):
    # TODO implement
    text = greeting()
    return {
        'statusCode': 200,
        'body': json.dumps(text)
    }
