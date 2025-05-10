import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["Tasks"])

def main(event, context):
    # Scan the DynamoDB table to get all tasks
    response = table.scan()
    items = response.get("Items", [])

    # Return the list of tasks
    return {
        "statusCode": 200,
        "body": json.dumps({"tasks": items}),
    }