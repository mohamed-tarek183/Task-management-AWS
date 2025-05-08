import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["Tasks"])

def main(event, context):
    # Scan the DynamoDB table to get all tasks
    task_id = event["pathParameters"]["id"]
    table.delete_item(Key={"id": task_id})
   

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Task {task_id} deleted"}),
    }