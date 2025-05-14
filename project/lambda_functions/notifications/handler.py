import boto3
import os

sqs = boto3.client('sqs', region_name='us-east-1')  
ses = boto3.client('ses', region_name='us-east-1')
SQS_URL=os.environ['SQS_QUEUE_URL']

def main(event, context):

    response=sqs.receive_message(
         QueueUrl=SQS_URL,
         WaitTimeSeconds=10,
         AttributeNames=['All'],       # Optional: to get extra metadata
         MessageAttributeNames=['All']
    )

    message=response.get("Messages",[])