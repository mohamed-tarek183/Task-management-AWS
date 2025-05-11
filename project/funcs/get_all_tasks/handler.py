import json
import boto3
import os
import pg8000
import traceback
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])
table_name=os.environ["DYNAMO_TABLE"]
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']

def main(event, context):
    task_ids=[]
    tasks=[]
    try:
        conn = pg8000.connect(
        host=db_host,        
        database=db_name, 
        user=db_user,   
        password=db_password
        )

        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

        cur = conn.cursor()

        cur.execute("SELECT task_id FROM user_tasks WHERE user_id=%s" , (user_id,))

        rows = cur.fetchall()
        

        task_ids = [str(row[0]) for row in rows]
        items=[]

        if task_ids:

  
            response = dynamodb.batch_get_item(
                RequestItems={
                    table_name: {
                        'Keys': [{'task_id': task_id} for task_id in task_ids]
                    }
                }
            )
            items = response['Responses'][table_name]  

            

        # Return the list of tasks
            return {
            "statusCode": 200,
            "body": json.dumps({"tasks": items}),
            "Num":len(task_ids)
        }


    except Exception as e:
        return {
        "statusCode": 500,
        "body": json.dumps({"error": traceback.format_exc()})
    }

