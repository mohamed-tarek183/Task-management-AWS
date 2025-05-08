import json
import uuid
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["Tasks"])

def main(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        if "title" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required field: title"})
            }

        task_id = str(uuid.uuid4())
        item = {
            "id": task_id,
            "title": body["title"],
            "completed": False
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps(item)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
