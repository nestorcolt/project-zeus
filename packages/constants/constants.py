"""

    Constants

"""

import inspect
import boto3
import os

# Account
ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

# Global vars
CURRENT_FRAME = inspect.getfile(inspect.currentframe())
ROOT_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FRAME)))
)
VERSION = "1.0.2"

# Logs
LOG_FILE_NAME = "bis_logs.txt"

# Zones
ZONE_US_EAST1 = "us-east-1b"

# Launch Template Ec2
AMI_ID = "ami-06d46e936b077fb88"
AMI_NAME = "ami-worker-ubuntu"
WORKER_LAUNCH_TEMPLATE_NAME = "Worker-Template"
KEY_PAIR_NAME = "worker-pem-file"
INSTANCE_TYPE = "t3a.micro"

# Security Groups Ec2
WORKER_SECURITY_GROUP_NAME = "Worker-SG"
WEB_SECURITY_GROUP_NAME = "WEB-APP-SG"

# VPC
VPC_NAME = "BIS-VPC"
VPC_CIDR_BLOCK = "172.31.0.0/16"

# Subnet
SUBNET_NAME = "BIS-Subnet"
SUBNET_CIDR_BLOCK = "172.31.0.0/20"
INTERNET_GATEWAY_NAME = "BIS-Int-Gateway"
ROUTE_TABLE_NAME = "BIS-Route-Table"

# Buckets
LAMBDA_BUCKET_NAME = "bis-serverless-s3"

# SNS
START_SE_SNS_NAME = "SE-START-SERVICE"
STOP_SE_SNS_NAME = "SE-STOP-SERVICE"
MODIFY_SE_SNS_NAME = "SE-MODIFY-SERVICE"
ACCEPTED_BLOCK_SNS_NAME = "SE-ACCEPTED-BLOCK-SERVICE"
INSTANCE_SLEEP_BLOCK_SNS_NAME = "SE-SLEEP-INSTANCE-SERVICE"
INSTANCE_WAKEUP_BLOCK_SNS_NAME = "SE-AWAKE-INSTANCE-SERVICE"

# SQS
SE_START_DEAD_LETTER_QUEUE = "SE-START-DLQ"
SE_MODIFY_DEAD_LETTER_QUEUE = "SE-MODIFY-DLQ"
SE_STOP_DEAD_LETTER_QUEUE = "SE-STOP-DLQ"
BLOCK_CAPTURED_DEAD_LETTER_QUEUE = "CB-DLQ"
INSTANCE_SLEEP_DEAD_LETTER_QUEUE = "INSTANCE-SLEEP-DLQ"
INSTANCE_AWAKE_DEAD_LETTER_QUEUE = "INSTANCE-AWAKE-DLQ"

# IAM
EC2_WORKER_IAM_INSTANCE_PROFILE = "ec2-worker-instance-profile"
EC2_TO_SNS_AND_S3_POLICY = "S3AndSnsEc2Policy"
EC2_WORKER_IAM_ROLE = "ec2-worker-iam-role"

# dynamo DB
USERS_TABLE_NAME = "Users"
BLOCKS_TABLE_NAME = "Blocks"

TABLE_PK = "user_id"
BLOCK_SORT_KEY = "block_id"
BLOCK_STATION_KEY = "station_id"
BLOCK_TIME_KEY = "block_time"
BLOCK_DATA_KEY = "data"
USER_LAST_ACTIVE_PROPERTY = "last_active"

# 28 minutes because the instance takes 3:52 minutes to start so will pass 31 minutes to send request again to FLEX
EC2_SLEEP_TIME_THRESHOLD = 28
CLEANUP_BLOCKS_TIME_THRESHOLD = 48  # Hours


# Web endpoints
WEB_BACKEND_ENDPOINT_URL = "XXXXX/api/blockNotification/sendAsync"