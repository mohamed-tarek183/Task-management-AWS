![Architecture](https://github.com/user-attachments/assets/bf0f30e5-51d4-44ff-878d-fc40aa06335e)# Welcome to your CDK Python project!

# Here is the project Architecture 
![Architecture](https://github.com/user-attachments/assets/4ca7c353-3549-46f0-a481-694ba9bae281)

# System Overview
This system is built to efficiently manage tasks and related operations through a scalable, secure, and serverless architecture powered by AWS. Below is an overview of the key features and architectural components.

# Core Functionalities
User Authentication and Management
Secure user sign-up, login, and session handling using AWS Cognito.

# Task Management
Create, update, and delete tasks via RESTful API endpoints.

# File Attachments
Upload and store task-related files securely using Amazon S3.

# Notifications
Notify users about task updates through asynchronous communication.

# Asynchronous Processing
Handle background jobs (e.g., notifications) via Amazon SQS.

# Architecture & Components
AWS Cloud (Top-Level)
All services are deployed within the AWS Cloud ecosystem, ensuring scalability and high availability.

# User Authentication
AWS Cognito manages user registration, authentication, and access control.

# API & Backend
Amazon API Gateway exposes secure REST API endpoints.

AWS Lambda processes API requests and executes backend logic for:

Task creation and updates

Metadata handling

Triggering notifications

# Application Hosting
VPC (Virtual Private Cloud) for network segmentation:

Public Subnet: Hosts the Web App Server

Private Subnet: Hosts internal backend resources

IAM Roles: Ensure secure and controlled access to AWS services.

# Data Storage
Amazon RDS: Stores structured data like user profiles and task metadata.

Amazon DynamoDB: Stores task details for fast and scalable access.

Amazon S3: Stores uploaded file attachments.

# Asynchronous Processing
Amazon SQS: Manages background jobs (e.g., email notifications) for non-blocking operations.

# Monitoring & Logging
AWS CloudWatch tracks metrics, errors, and resource utilization across all services:

Lambda

API Gateway

EC2

RDS and more

Dashboards and alarms help monitor performance and trigger alerts when needed.

# External Access
Web Client (Next.js + TypeScript): Allows users to interact with the system.

Communicates with backend via REST APIs through API Gateway.

# Flow of Operation
User Authentication
The user logs in via the web client using AWS Cognito.

Task Creation

Authenticated user creates a task via the web interface.

The request is routed through API Gateway and handled by a Lambda function.

Task data is stored in both DynamoDB and RDS.

Any file attachments are uploaded to S3.

Task Updates & Notifications

On task updates, messages are pushed to SQS.

SQS triggers background Lambda jobs to send notifications to users (e.g., email).

System Monitoring

CloudWatch logs and monitors system performance, raising alerts for anomalies.

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
