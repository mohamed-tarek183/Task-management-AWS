from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_cognito as cognito,
    aws_sqs as sqs,
    aws_logs as logs,
    Duration,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct
import os


class LambdaApiGatewayConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            id: str,
            *,
            cognito_user_pool=None,
            dynamo_table=None,
            s3_bucket=None,
            notification_queue=None,
            lambda_role=None,
            **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Common environment variables for Lambda functions
        lambda_env = {
            "DYNAMODB_TABLE": dynamo_table.table_name if dynamo_table else "",
            "S3_BUCKET": s3_bucket.bucket_name if s3_bucket else "",
            "SQS_QUEUE_URL": notification_queue.queue_url if notification_queue else ""
        }

        # Create Lambda functions for task operations
        self.get_tasks_lambda = lambda_.Function(
            self, "GetTasksFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="get_tasks.handler",
            code=lambda_.Code.from_asset("project/lambda/tasks"),
            timeout=Duration.seconds(30),
            environment=lambda_env,
            role=lambda_role,
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        self.get_task_lambda = lambda_.Function(
            self, "GetTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="get_task.handler",
            code=lambda_.Code.from_asset("project/lambda/tasks"),
            timeout=Duration.seconds(30),
            environment=lambda_env,
            role=lambda_role,
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        self.create_task_lambda = lambda_.Function(
            self, "CreateTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="create_task.handler",
            code=lambda_.Code.from_asset("project/lambda/tasks"),
            timeout=Duration.seconds(30),
            environment=lambda_env,
            role=lambda_role,
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        self.update_task_lambda = lambda_.Function(
            self, "UpdateTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="update_task.handler",
            code=lambda_.Code.from_asset("project/lambda/tasks"),
            timeout=Duration.seconds(30),
            environment=lambda_env,
            role=lambda_role,
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        self.delete_task_lambda = lambda_.Function(
            self, "DeleteTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="delete_task.handler",
            code=lambda_.Code.from_asset("project/lambda/tasks"),
            timeout=Duration.seconds(30),
            environment=lambda_env,
            role=lambda_role,
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        # File upload function
        self.upload_attachment_lambda = lambda_.Function(
            self, "UploadAttachmentFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="upload_attachment.handler",
            code=lambda_.Code.from_asset("project/lambda/files"),
            timeout=Duration.seconds(30),
            environment=lambda_env,
            role=lambda_role,
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        # Create API Gateway
        self.api = apigateway.RestApi(
            self, "TaskManagerApi",
            rest_api_name="Task Manager API",
            description="API for Task Management System",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "Authorization", "X-Amz-Date", "X-Api-Key"]
            )
        )

        # Add Cognito authorizer if user pool provided
        authorizer = None
        if cognito_user_pool:
            authorizer = apigateway.CognitoUserPoolsAuthorizer(
                self, "TasksAuthorizer",
                cognito_user_pools=[cognito_user_pool]
            )

        # Define auth_type based on whether authorizer exists
        auth_type = apigateway.AuthorizationType.COGNITO if authorizer else apigateway.AuthorizationType.NONE

        # Add routes to API Gateway
        # Tasks resource
        tasks = self.api.root.add_resource("tasks")

        # GET /tasks
        tasks.add_method(
            "GET",
            apigateway.LambdaIntegration(self.get_tasks_lambda),
            authorizer=authorizer,
            authorization_type=auth_type
        )

        # POST /tasks
        tasks.add_method(
            "POST",
            apigateway.LambdaIntegration(self.create_task_lambda),
            authorizer=authorizer,
            authorization_type=auth_type
        )

        # Single task resource
        task = tasks.add_resource("{taskId}")

        # GET /tasks/{taskId}
        task.add_method(
            "GET",
            apigateway.LambdaIntegration(self.get_task_lambda),
            authorizer=authorizer,
            authorization_type=auth_type
        )

        # PUT /tasks/{taskId}
        task.add_method(
            "PUT",
            apigateway.LambdaIntegration(self.update_task_lambda),
            authorizer=authorizer,
            authorization_type=auth_type
        )

        # DELETE /tasks/{taskId}
        task.add_method(
            "DELETE",
            apigateway.LambdaIntegration(self.delete_task_lambda),
            authorizer=authorizer,
            authorization_type=auth_type
        )

        # Attachment resource
        attachments = task.add_resource("attachments")

        # POST /tasks/{taskId}/attachments
        attachments.add_method(
            "POST",
            apigateway.LambdaIntegration(self.upload_attachment_lambda),
            authorizer=authorizer,
            authorization_type=auth_type
        )

        # Output the API URL
        CfnOutput(
            self, "ApiUrl",
            value=self.api.url,
            description="URL of the Task Manager API"
        )