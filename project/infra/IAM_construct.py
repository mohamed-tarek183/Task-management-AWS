from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_cognito as cognito,
    aws_lambda as lambda_,
)
from constructs import Construct


class IAMConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            id: str,
            *,
            s3_bucket=None,
            dynamodb_table=None,
            **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # EC2 Role - allows EC2 to interact with other services
        self.ec2_role = iam.Role(
            self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ],
            description="Role for EC2 instances in Task Management System"
        )

        # Add S3 read/write permissions if bucket provided
        if s3_bucket:
            s3_bucket.grant_read_write(self.ec2_role)

        # Add DynamoDB permissions if table provided
        if dynamodb_table:
            dynamodb_table.grant_read_write_data(self.ec2_role)

        # Lambda execution role for task management
        self.lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ],
            description="Role for Lambda functions in Task Management System"
        )

        # Add appropriate permissions to Lambda role
        if s3_bucket:
            s3_bucket.grant_read_write(self.lambda_role)

        if dynamodb_table:
            dynamodb_table.grant_read_write_data(self.lambda_role)

        # Custom policy for RDS access
        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "rds-data:ExecuteStatement",
                    "rds-data:BatchExecuteStatement",
                    "rds:DescribeDBClusters"
                ],
                resources=["*"]  # Restrict this to specific RDS ARN in production
            )
        )

        # Add CloudWatch logs permissions
        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                resources=["arn:aws:logs:*:*:*"]
            )
        )

        # Add SQS permissions
        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "sqs:SendMessage",
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes"
                ],
                resources=["*"]  # Restrict this to specific SQS ARN in production
            )
        )