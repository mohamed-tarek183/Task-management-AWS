from aws_cdk import (
    Duration,
    Stack,
    NestedStack,
    RemovalPolicy
)
import aws_cdk.aws_secretsmanager as secretsmanager

from aws_cdk import aws_ec2 as ec2, aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from .EC2_construct import EC2InstanceConstruct

from .RDS_construct import RDSInstanceConstruct


class infra_stack(NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.vpc=ec2.Vpc(self,"MyVPC",
        max_azs=2,
        nat_gateways=0,
        subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ]
        )

        self.vpc.apply_removal_policy(RemovalPolicy.DESTROY)

        self.ec2=EC2InstanceConstruct(self, "EC2",vpc=self.vpc)

        self.rds=RDSInstanceConstruct(self,"RDS",
                             vpc=self.vpc,
                             db_name="Task_Mangement",
                             db_username="adminusr",
                             db_password="adminpwrd"
        )

        self.s3=s3.Bucket(self,"Task_Mangement_Attachments",
                        removal_policy=RemovalPolicy.DESTROY,  # For dev/testing — delete bucket on stack destroy
                        auto_delete_objects=True)
        
        self.dynamo_db=dynamodb.TableV2(self,"Task_Metadata",
                                        partition_key=dynamodb.Attribute(
                                        name="task_id",
                                        type=dynamodb.AttributeType.STRING
                                        ),table_name="metadata",
                                        billing=dynamodb.Billing.on_demand(),
                                        removal_policy=RemovalPolicy.DESTROY    
                                        )


        self.vpc.add_gateway_endpoint("S3_Endpoint",
                            service=ec2.GatewayVpcEndpointAwsService.S3)
        
        self.vpc.add_gateway_endpoint("DynamoDB_Endpoint",
                            service=ec2.GatewayVpcEndpointAwsService.DYNAMODB)
        


        self.dynamo_table=self.dynamo_db.table_name
        self.rds_host=self.rds.rds_host
        self.rds_port=self.rds.rds_port
        self.rds_db_name="Task_Mangement"
        self.rds_username="adminusr"
        self.rds_password="adminpwrd"
        self.s3_arn=self.s3.bucket_arn
        self.s3_bucket_name=self.s3.bucket_name
        