import aws_cdk as core
import aws_cdk.assertions as assertions
from project.project_stack import ProjectStack


def test_sns_topic_created():
    # Arrange
    app = core.App()
    stack = ProjectStack(app, "project")
    
    # Act
    template = assertions.Template.from_stack(stack)

    # Assert: Ensure SNS Topic is created
    template.has_resource_properties("AWS::SNS::Topic", {
        "Subscription": [{
            "Endpoint": "santhosh.kumar@gmail.com",  # Replace with your email for testing
            "Protocol": "email"
        }]
    })


def test_cloudwatch_alarm_created():
    # Arrange
    app = core.App()
    stack = ProjectStack(app, "project")
    
    # Act
    template = assertions.Template.from_stack(stack)

    # Assert: Ensure CloudWatch Alarm for Lambda Errors is created
    template.has_resource_properties("AWS::CloudWatch::Alarm", {
        "AlarmActions": [{
            "Ref": "CloudWatchAlarmTopic"  # SNS topic reference
        }],
        "MetricName": "Errors",
        "Namespace": "AWS/Lambda",
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "Threshold": 1
    })

    # Assert: Ensure CloudWatch Alarm for EC2 CPU Utilization is created
    template.has_resource_properties("AWS::CloudWatch::Alarm", {
        "AlarmActions": [{
            "Ref": "CloudWatchAlarmTopic"  # SNS topic reference
        }],
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "Threshold": 80
    })

    # Assert: Ensure CloudWatch Alarm for RDS High CPU Usage is created
    template.has_resource_properties("AWS::CloudWatch::Alarm", {
        "AlarmActions": [{
            "Ref": "CloudWatchAlarmTopic"  # SNS topic reference
        }],
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/RDS",
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "Threshold": 85
    })


def test_dynamodb_throttling_alarm():
    # Arrange
    app = core.App()
    stack = ProjectStack(app, "project")
    
    # Act
    template = assertions.Template.from_stack(stack)

    # Assert: Ensure DynamoDB throttling alarm is created
    template.has_resource_properties("AWS::CloudWatch::Alarm", {
        "MetricName": "ThrottledRequests",
        "Namespace": "AWS/DynamoDB",
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "Threshold": 1
    })
