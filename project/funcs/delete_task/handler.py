import json
import boto3
import os
import pg8000
dynamodb = boto3.resource("dynamodb")
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

    
    # Scan the DynamoDB table to get all tasks
    task_id = event["pathParameters"]["id"]
    table.delete_item(Key={"task_id": task_id})

    cur.execute("DELETE FROM user_tasks WHERE task_id = %s", (task_id))


    conn.commit()
    cur.close()
    conn.close()
   

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Task {task_id} deleted"}),
    }