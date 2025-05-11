import json
import uuid
import boto3
import os

s3_bucket = os.environ['S3_BUCKET']
s3_client = boto3.client('s3')

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])

def main(event, context):
    try:
        # Log the event for debugging

        body = json.loads(event.get("body", "{}"))

        task_id = body['task_id']

        file_name = body['file_name']

        response = table.get_item(
            Key={'task_id': task_id}  # Assuming 'task_id' is the partition key in your DynamoDB table
        )
        
        # Check if the item exists
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Task ID not found in DynamoDB"})
            }

        object_name = f"{task_id}/{file_name}"

        response = s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': s3_bucket, 'Key': object_name},
                ExpiresIn=3600
            )
        
        return {
            "statusCode": 201,
            "URL": response
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "TI":task_id,
            "body": json.dumps({"error": str(e)})
        }
