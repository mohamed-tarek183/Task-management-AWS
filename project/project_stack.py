from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    # aws_sqs as sqs,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,  # Import DynamoDB
    RemovalPolicy,
)

from constructs import Construct
from project.infra.infra_stack import infra_stack
import os

class ProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        def create_lambda(id: str, folder: str):
            return _lambda.Function(
                self, id,
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler="handler.main",
                code=_lambda.Code.from_asset(os.path.join("project", "lambda", folder))
    )
        
        # Create Lambda functions
        create_task_func = create_lambda("CreateTaskFunction", "create_task")
        update_task_func = create_lambda("UpdateTaskFunction", "update_task")
        delete_task_func = create_lambda("DeleteTaskFunction", "delete_task")
        get_task_func = create_lambda("GetTaskFunction", "get_task")
        get_all_tasks_func = create_lambda("GetAllTasksFunction", "get_all_tasks")

        # Define the DynamoDB table
        table = ddb.Table(
            self, "Tasks",
            partition_key=ddb.Attribute(name="id", type=ddb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY  # WARNING: Use only for development
        )

        # Grant permissions and add environment variables to Lambda functions
        for fn in [create_task_func, delete_task_func, get_task_func, update_task_func, get_all_tasks_func]:
            table.grant_read_write_data(fn)
            fn.add_environment("Tasks", table.table_name)

        # Define API Gateway
        api = apigw.RestApi(self, "TaskApi", rest_api_name="Task Service")
        
        tasks = api.root.add_resource("tasks")
        tasks.add_method("POST", apigw.LambdaIntegration(create_task_func))
        tasks.add_method("GET", apigw.LambdaIntegration(get_all_tasks_func))

        task = tasks.add_resource("{id}")
        task.add_method("GET", apigw.LambdaIntegration(get_task_func))
        task.add_method("PUT", apigw.LambdaIntegration(update_task_func))
        task.add_method("DELETE", apigw.LambdaIntegration(delete_task_func))

        # Infrastructure stack
        self.infra = infra_stack(self, "InfraStack")
