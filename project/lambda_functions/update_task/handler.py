import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])

def main(event, context):
    try:
        task_id = event["pathParameters"]["task_id"]
        if not task_id:
            return {
                "statusCode": 400,
                'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
                "body": json.dumps({"error": "Missing task ID in path parameters"})
            }

        body = json.loads(event.get("body", "{}"))

        if "title" not in body:
            return {
                "statusCode": 400,
                'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
                "body": json.dumps({"error": "Missing required field: title"})
            }

        response = table.update_item(
            Key={"task_id": task_id},
            UpdateExpression="SET title = :title, completed = :completed , dueDate=:dueDate , priority=:priority , description=:description",
            ExpressionAttributeValues={
                ":title": body["title"],
                ":completed": body["completed"],
                ":dueDate":body["dueDate"],
                ":priority":body["priority"],
                ":description":body["description"]
            },
            ReturnValues="ALL_NEW"
        )

        return {
            "statusCode": 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
            "body": json.dumps(response["Attributes"])
        }

    except Exception as e:
        return {
            "statusCode": 500,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
            "body": json.dumps({"error": str(e)})
        }
