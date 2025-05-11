import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])

s3_bucket = os.environ['S3_BUCKET']
s3_client = boto3.client('s3')

def main(event, context):
    task_id = event["pathParameters"]["task_id"]

    response = table.get_item(Key={"task_id": task_id})
    item = response.get("Item")

    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Task not found"}),
        }

    prefix = f"{task_id}/"
    files = []

    response = s3_client.list_objects_v2(
        Bucket=s3_bucket,
        Prefix=prefix  
    )
    
    if 'Contents' in response:
        files = [obj['Key'] for obj in response['Contents']]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "task": item,  
            "attachments": files  
        })
    }
