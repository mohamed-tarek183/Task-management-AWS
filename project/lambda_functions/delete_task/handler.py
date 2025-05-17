import json
import boto3
import os
import pg8000
s3 = boto3.client('s3')
dynamodb = boto3.resource("dynamodb")
S3_BUCKET = os.environ.get('S3_BUCKET')
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']


def main(event, context):
    conn = pg8000.connect(
        host=db_host,        
        database=db_name, 
        user=db_user,   
        password=db_password
        )
    
    cur = conn.cursor()

    
    task_id = event["pathParameters"]["task_id"]
    table.delete_item(Key={"task_id": task_id})
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=f"{task_id}/")

    if 'Contents' not in response:
        return
    objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

    # Delete objects in batch (up to 1000 per call)
    delete_response = s3.delete_objects(
        Bucket=S3_BUCKET,
        Delete={'Objects': objects_to_delete}
    )


    cur.execute("DELETE FROM user_tasks WHERE task_id = %s", (task_id,))


    conn.commit()
    cur.close()
    conn.close()
   

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Task {task_id} deleted"}),
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
             "Content-Type": "application/json"
        }
    }