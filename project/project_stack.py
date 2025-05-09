from aws_cdk import (
    # Duration,
    Stack,
    core,
    # aws_sqs as sqs,
)
from project.infra.cloudwatch_stack import CloudWatchStack
from constructs import Construct
from project.infra.infra_stack import infra_stack

class ProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.infra = infra_stack(self, "InfraStack")
        self.cloudwatch = CloudWatchStack(self, "CloudWatchStack")
