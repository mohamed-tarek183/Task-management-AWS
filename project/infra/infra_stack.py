from aws_cdk import (
    Duration,
    Stack,
    NestedStack,
    RemovalPolicy
)

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

        #VPC setup with 2 AZs , 2 subnets in each AZ (1 Private, 1 Public)
        self.vpc=ec2.Vpc(self,"MyVPC",
        max_azs=1,
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

        public_subnets = self.vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnets
        private_subnets = self.vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets


        self.ec2=EC2InstanceConstruct(self, "EC2",
                vpc=self.vpc,
                subnet=public_subnets[0],
        )

        
        

        # self.rds=RDSInstanceConstruct(self,"RDS",
        #                      vpc=self.vpc,
        #                      subnet=private_subnets[0],
        #                      db_name="Task_Mangement",
        #                      db_username="admin",
        #                      db_password="admin"
        # )

        self.s3=s3.Bucket(self,"Task_Mangement_Attachments",
                        removal_policy=RemovalPolicy.DESTROY,  # For dev/testing — delete bucket on stack destroy
                        auto_delete_objects=True)
        

        # self.vpc.add_gateway_endpoint("S3_Endpoint",
        #                     service=ec2.GatewayVpcEndpointAwsService.S3,
        #                     subnets=[private_subnets[0]],)