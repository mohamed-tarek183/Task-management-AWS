import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["Tasks"])


def main(event, context):
    task_id = event["pathParameters"]["id"]

     # Mock response
    response = table.get_item(
        Key={"id": task_id}
    )
    item = response.get("Item")

    if not item: 
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Task not found"}),
        }
    return {
        "statusCode": 200,
        "body": json.dumps({"task": response["Item"]}),
    }

