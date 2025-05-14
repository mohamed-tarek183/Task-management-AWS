from aws_cdk import (
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_events,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subs,
    Duration,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct


class SQSConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            id: str,
            *,
            lambda_role=None,
            **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Create Dead-Letter Queue for failed message processing
        self.dlq = sqs.Queue(
            self, "NotificationDLQ",
            visibility_timeout=Duration.seconds(300),
            retention_period=Duration.days(14),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create notification queue with DLQ configuration
        self.notification_queue = sqs.Queue(
            self, "NotificationQueue",
            queue_name="NotificationQueue.fifo",
            fifo=True,
            content_based_deduplication=True,
            visibility_timeout=Duration.seconds(300),
            retention_period=Duration.days(4),
            removal_policy=RemovalPolicy.DESTROY,
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=5,  # After 3 failed processing attempts, send to DLQ
                queue=self.dlq
            ),
            
        )

        # Create SNS Topic for task events
        # self.task_events_topic = sns.Topic(
        #     self, "TaskEventsTopic",
        #     display_name="Task Management Events"
        # )

        # # Subscribe the SQS queue to the SNS topic
        # self.task_events_topic.add_subscription(
        #     sns_subs.SqsSubscription(self.notification_queue)
        # )

        #Create notification processor Lambda
        self.notification_processor = lambda_.Function(
            self, "NotificationProcessor",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="main.handler",
            code=lambda_.Code.from_asset("project/lambda_functions/notifications"),
            timeout=Duration.seconds(60),
            environment={
                "SQS_QUEUE_URL": self.notification_queue.queue_url
            },
            role=lambda_role
        )

        # Add SQS event source to Lambda
        self.notification_processor.add_event_source(
            lambda_events.SqsEventSource(
                self.notification_queue,
                batch_size=10,  # Process 10 messages at once
                max_batching_window=Duration.seconds(30)  # Wait up to 30 seconds to collect messages
            )
        )

        # Output information
        CfnOutput(
            self, "NotificationQueueUrl",
            value=self.notification_queue.queue_url,
            description="URL of the Notification SQS Queue"
        )

        CfnOutput(
            self, "NotificationDLQUrl",
            value=self.dlq.queue_url,
            description="URL of the Dead-Letter Queue for failed notifications"
        )

        CfnOutput(
            self, "TaskEventsTopicArn",
            value=self.task_events_topic.topic_arn,
            description="ARN of the Task Events SNS Topic"
        )
