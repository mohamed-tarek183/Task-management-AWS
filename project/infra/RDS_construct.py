from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Duration,
    RemovalPolicy,
    aws_rds as rds,
    SecretValue

)
from constructs import Construct


class RDSInstanceConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc: ec2.Vpc,
        db_name: str,
        db_username: str,
        db_password: str,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)


        self.security_group = ec2.SecurityGroup(
            self, f"{id}RDS_SG",
            vpc=vpc,
            description=f"Security group for RDS {id}",
            allow_all_outbound=True
        )


        self.security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "Allow Postgres access"
        )

        # Create the RDS instance (using MySQL in this case)
        self.rds_instance = rds.DatabaseInstance(
            self, id,
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            instance_type=ec2.InstanceType("t3.micro"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            database_name=db_name,
            credentials=rds.Credentials.from_password(
                username=db_username,  
                password=SecretValue.unsafe_plain_text(db_password)  # Your hardcoded password
            ),
            multi_az=False,
            allocated_storage=20, 
            security_groups=[self.security_group], 
            removal_policy=RemovalPolicy.RETAIN, 
            publicly_accessible=False 
        )
      


        