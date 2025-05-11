from aws_cdk import (
    Duration,
    Stack,
    NestedStack,
    RemovalPolicy,
    aws_lambda as lambda_,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class lambda_stack(NestedStack):
    def __init__(self, scope: Construct, id: str,db_config:dict,vpc,**kwargs,):
        super().__init__(scope, id, **kwargs)

        # env={
        #     "DYNAMO_TABLE": db_config['DYNAMO_TABLE'],
        #     "DB_HOST":db_config['DB_HOST'],
        #     "DB_NAME":db_config['DB_NAME'],
        #     "DB_USER":db_config['DB_USER'],
        #     "DB_PASSWORD":db_config['DB_PASSWORD'],
        #     "S3_BUCKET":db_config['S3_BUCKET']
        #     } 
        lambda_layer = lambda_.LayerVersion(
        self, 'LambdaLayer',
        code=lambda_.Code.from_asset('project/funcs/lambda_layer/my-lambda-layer.zip'),
        compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
        description="PostgreSQL dependencies layer")



        self.create_func=lambda_.Function(
            self,"Create Task Lambda Function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="handler.main",
            code=lambda_.Code.from_asset("project/funcs/create_task"),
            timeout=Duration.seconds(30),
            layers=[lambda_layer],
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            environment=db_config
            )
        



        self.delete_func=lambda_.Function(
            self,"Delete Task Lambda Function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="handler.main",
            code=lambda_.Code.from_asset("project/funcs/delete_task"),
            timeout=Duration.seconds(30),
            layers=[lambda_layer],
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            environment=db_config
            )
        

        self.update_func=lambda_.Function(
            self,"Update Task Lambda Function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="handler.main",
            code=lambda_.Code.from_asset("project/funcs/update_task"),
            timeout=Duration.seconds(30),
            layers=[lambda_layer],
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            environment=db_config
            )
        

        self.get_func=lambda_.Function(
            self,"Get Task Lambda Function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="handler.main",
            code=lambda_.Code.from_asset("project/funcs/get_task"),
            timeout=Duration.seconds(30),
            layers=[lambda_layer],
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            environment=db_config
            )
        
        self.get_all_func=lambda_.Function(
            self,"Get All Tasks Lambda Function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="handler.main",
            code=lambda_.Code.from_asset("project/funcs/get_all_tasks"),
            timeout=Duration.seconds(30),
            layers=[lambda_layer],
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            environment=db_config
            )
        


        self.upload_file_func=lambda_.Function(
            self,"Upload File to S3 Lambda Function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="handler.main",
            code=lambda_.Code.from_asset("project/funcs/upload_file"),
            timeout=Duration.seconds(30),
            layers=[lambda_layer],
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            environment=db_config
            )
        


        self.delete_func.add_to_role_policy(iam.PolicyStatement(
        actions=["dynamodb:DeleteItem"],
        resources=["arn:aws:dynamodb:eu-central-1:614965295050:table/metadata"]))
        
        self.create_func.add_to_role_policy(iam.PolicyStatement(
        actions=["dynamodb:PutItem"],
        resources=["arn:aws:dynamodb:eu-central-1:614965295050:table/metadata"]))
        
        self.update_func.add_to_role_policy(iam.PolicyStatement(
        actions=["dynamodb:UpdateItem"],
        resources=["arn:aws:dynamodb:eu-central-1:614965295050:table/metadata"]))
        
        self.get_func.add_to_role_policy(iam.PolicyStatement(
        actions=["dynamodb:GetItem"],
        resources=["arn:aws:dynamodb:eu-central-1:614965295050:table/metadata"]))

        self.get_all_func.add_to_role_policy(iam.PolicyStatement(
        actions=["s3:PutObject", "s3:ListBucket"],
        resources=[
            "arn:aws:s3:::your-bucket-name/*",  # For objects in the bucket
            "arn:aws:s3:::your-bucket-name"     # For listing the bucket
        ]
 
)) 

        self.upload_file_func.add_to_role_policy(iam.PolicyStatement(
        actions=["dynamodb:GetItem"],
        resources=["arn:aws:dynamodb:eu-central-1:614965295050:table/metadata"]))



        self.upload_file_func.add_to_role_policy(iam.PolicyStatement(
        actions=["s3:PutObject", "s3:ListBucket"],
        resources=[
            "arn:aws:s3:::projectstack-infrastackne-taskmangementattachments-rqgdz17dxibh/*",  # For objects in the bucket
            "arn:aws:s3:::projectstack-infrastackne-taskmangementattachments-rqgdz17dxibh"     # For listing the bucket
        ]
))

        self.get_func.add_to_role_policy(iam.PolicyStatement(
        actions=["s3:PutObject", "s3:ListBucket"],
        resources=[
            "arn:aws:s3:::projectstack-infrastackne-taskmangementattachments-rqgdz17dxibh/*",  # For objects in the bucket
            "arn:aws:s3:::projectstack-infrastackne-taskmangementattachments-rqgdz17dxibh"     # For listing the bucket
        ]
))  