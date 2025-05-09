from aws_cdk import Stack, Duration
import aws_cdk.aws_cloudwatch as cw
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as subs
import aws_cdk.aws_cloudwatch_actions as cw_actions
from aws_cdk import aws_rds as rds
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_sqs as sqs
from constructs import Construct

class CloudWatchStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create SNS topic to send alarm notifications
        topic = sns.Topic(self, "CloudWatchAlarmTopic")
        
        # Add email subscription for SNS topic
        topic.add_subscription(subs.EmailSubscription("santhosh.kumar@gmail.com"))

        # Define Lambda function (Example)
        lambda_function = _lambda.Function(
            self, "TaskManagementLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_inline("""
import json

def handler(event, context):
    print('Lambda function triggered')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
            """)
        )

        # CloudWatch Logs for Lambda
        log_group = cw.LogGroup(self, "LambdaLogGroup", 
            log_group_name=f"/aws/lambda/{lambda_function.function_name}"
        )

        # Create CloudWatch Metric for Lambda Errors
        lambda_error_metric = cw.Metric(
            namespace="AWS/Lambda",
            metric_name="Errors",
            dimensions_map={"FunctionName": lambda_function.function_name},
            statistic="Sum",
            period=Duration.minutes(5),
        )

        # Create CloudWatch Alarm for Lambda Errors
        lambda_error_alarm = cw.Alarm(
            self, "LambdaErrorAlarm",
            metric=lambda_error_metric,
            threshold=1,
            evaluation_periods=1,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            actions=[cw_actions.SnsAction(topic)]  # Send notification to SNS
        )

        # API Gateway Metrics (Example)
        api_gateway = apigateway.RestApi(self, "TaskAPI")
        
        api_latency_metric = cw.Metric(
            namespace="AWS/ApiGateway",
            metric_name="Latency",
            dimensions_map={"ApiName": api_gateway.rest_api_name},
            statistic="Average",
            period=Duration.minutes(5),
        )

        # Create CloudWatch Alarm for API Gateway Latency
        api_gateway_alarm = cw.Alarm(
            self, "ApiGatewayLatencyAlarm",
            metric=api_latency_metric,
            threshold=2,  # example latency threshold in seconds
            evaluation_periods=2,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            actions=[cw_actions.SnsAction(topic)]  # Send notification to SNS
        )

        # EC2 Monitoring
        instance = ec2.Instance(self, "MyEC2Instance", ...)  # Replace with actual EC2 creation logic
        ec2_metric = cw.Metric(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",
            dimensions_map={"InstanceId": instance.instance_id},
            statistic="Average",
            period=Duration.minutes(5)
        )

        ec2_alarm = cw.Alarm(
            self, "EC2HighCpuAlarm",
            metric=ec2_metric,
            threshold=80,
            evaluation_periods=2,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            actions=[cw_actions.SnsAction(topic)]  # Send notification to SNS
        )

        # RDS Monitoring
        rds_instance = rds.DatabaseInstance(self, "MyRDSInstance", ...)  # Replace with actual RDS creation logic
        rds_metric = cw.Metric(
            namespace="AWS/RDS",
            metric_name="CPUUtilization",
            dimensions_map={"DBInstanceIdentifier": rds_instance.instance_identifier},
            statistic="Average",
            period=Duration.minutes(5),
        )

        rds_alarm = cw.Alarm(
            self, "RDSHighCpuAlarm",
            metric=rds_metric,
            threshold=85,  # Adjust CPU threshold
            evaluation_periods=2,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            actions=[cw_actions.SnsAction(topic)]  # Send notification to SNS
        )

        # DynamoDB Monitoring
        dynamo_read_metric = cw.Metric(
            namespace="AWS/DynamoDB",
            metric_name="ConsumedReadCapacityUnits",
            dimensions_map={"TableName": "Task_Metadata"},
            statistic="Sum",
            period=Duration.minutes(5),
        )

        dynamo_throttled_metric = cw.Metric(
            namespace="AWS/DynamoDB",
            metric_name="ThrottledRequests",
            dimensions_map={"TableName": "Task_Metadata"},
            statistic="Sum",
            period=Duration.minutes(5),
        )

        dynamo_throttled_alarm = cw.Alarm(
            self, "DynamoDBThrottledRequestsAlarm",
            metric=dynamo_throttled_metric,
            threshold=1,
            evaluation_periods=2,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            actions=[cw_actions.SnsAction(topic)]  # Send notification to SNS
        )

        # S3 Monitoring
        s3_bucket = s3.Bucket(self, "TaskAttachmentsBucket", ...)
        s3_put_metric = cw.Metric(
            namespace="AWS/S3",
            metric_name="PutRequest",
            dimensions_map={"BucketName": s3_bucket.bucket_name, "StorageType": "AllStorageTypes"},
            statistic="Sum",
            period=Duration.minutes(5),
        )

        s3_put_alarm = cw.Alarm(
            self, "S3PutRequestsAlarm",
            metric=s3_put_metric,
            threshold=1000,  # Adjust based on your needs
            evaluation_periods=2,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            actions=[cw_actions.SnsAction(topic)]  # Send notification to SNS
        )

        # SQS Monitoring
        sqs_queue = sqs.Queue(self, "TaskQueue", ...)  # Replace with actual SQS creation logic
        sqs_messages_metric = cw.Metric(
            namespace="AWS/SQS",
            metric_name="ApproximateNumberOfMessagesVisible",
            dimensions_map={"QueueName": sqs_queue.queue_name},
            statistic="Average",
            period=Duration.minutes(5),
        )

        sqs_alarm = cw.Alarm(
            self, "SQSQueueLengthAlarm",
            metric=sqs_messages_metric,
            threshold=10,  # Adjust based on your needs
            evaluation_periods=2,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            actions=[cw_actions.SnsAction(topic)]  # Send notification to SNS
        )

        # CloudWatch Dashboard
        dashboard = cw.Dashboard(self, "CloudWatchDashboard")
        dashboard.add_widgets(
            cw.GraphWidget(title="EC2 CPU Utilization", left=[ec2_metric]),
            cw.GraphWidget(title="Lambda Errors", left=[lambda_error_metric]),
            cw.GraphWidget(title="API Gateway Latency", left=[api_latency_metric]),
            cw.GraphWidget(title="RDS CPU Utilization", left=[rds_metric]),
            cw.GraphWidget(title="DynamoDB Throttled Requests", left=[dynamo_throttled_metric]),
            cw.GraphWidget(title="S3 Put Requests", left=[s3_put_metric]),
            cw.GraphWidget(title="SQS Queue Length", left=[sqs_messages_metric])
        )
