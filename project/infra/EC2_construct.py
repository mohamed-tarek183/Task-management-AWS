from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Duration,
    RemovalPolicy
)
from constructs import Construct
class EC2InstanceConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc: ec2.Vpc,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        self.security_group = ec2.SecurityGroup(
            self, "InstanceSG",
            vpc=vpc,
            description=f"Security group for {id}",
            allow_all_outbound=True
        )


        self.security_group.add_ingress_rule(
                peer=ec2.Peer.any_ipv4(),
                connection=ec2.Port.tcp(22),
                description="Allow SSH access"
            )

        self.security_group.add_ingress_rule(
                peer=ec2.Peer.any_ipv4(),
                connection=ec2.Port.tcp(80),
                description="Allow HTTP access"
            )
        

        key_pair = ec2.KeyPair.from_key_pair_name(
            self, 
            "ImportedKeyPair",
            key_pair_name="mohtarek"  # This should match the name in AWS console
        )
        


        self.instance = ec2.Instance(
            self, id,
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=self.security_group,
            key_name=key_pair.key_pair_name
        )
        


        