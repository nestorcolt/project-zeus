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
USER_PLACEHOLDER = "User-{}"

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
VPC_CIDR_BLOCK = "172.31.0.0/16"
VPC_NAME = "BIS-VPC"

# Subnet
INTERNET_GATEWAY_NAME = "BIS-Int-Gateway"
ROUTE_TABLE_NAME = "BIS-Route-Table"
SUBNET_CIDR_BLOCK = "172.31.0.0/20"
SUBNET_NAME = "BIS-Subnet"

# Buckets
LAMBDA_BUCKET_NAME = "bis-serverless-s3"

# SNS
SE_AUTHENTICATE_TOPIC = "SE-AUTHENTICATE-TOPIC"
SE_ACCEPTED_TOPIC = "SE-ACCEPTED-TOPIC"
SE_START_TOPIC = "SE-START-TOPIC"
SE_OFFERS_TOPIC = "SE-OFFERS-TOPIC"
SE_SLEEP_TOPIC = "SE-SLEEP-TOPIC"
SE_ERROR_TOPIC = "SE-ERROR-TOPIC"
SE_LOGS_TOPIC = "SE-LOGS-TOPIC"

# SQS
SE_AUTHENTICATE_DLQ = "SE-AUTHENTICATE-DLQ"
SE_ACCEPTED_DLQ = "SE-ACCEPTED-DLQ"
SE_OFFERS_DLQ = "SE-OFFERS-DLQ"
SE_START_DLQ = "SE-START-DLQ"
SE_ERROR_DLQ = "SE-ERROR-DLQ"
SE_SLEEP_DLQ = "SE-SLEEP-DLQ"
SE_LOGS_DLQ = "SE-LOGS-DLQ"
SE_ON_PROCESS = "SeOnProcessQueue"

# IAM
EC2_WORKER_IAM_INSTANCE_PROFILE = "ec2-worker-instance-profile"
EC2_TO_SNS_AND_S3_POLICY = "S3AndSnsEc2Policy"
EC2_WORKER_IAM_ROLE = "ec2-worker-iam-role"

# dynamo DB
BLOCKS_TABLE_NAME = "Blocks"
OFFERS_TABLE_NAME = "Offers"
USERS_TABLE_NAME = "Users"

USER_LAST_ACTIVE_PROPERTY = "last_active"
BLOCK_STATION_KEY = "station_id"
BLOCK_TIME_KEY = "block_time"
BLOCK_SORT_KEY = "block_id"
BLOCK_DATA_KEY = "data"
TABLE_PK = "user_id"

OFFER_STATION_ID = BLOCK_STATION_KEY
OFFER_DATA_KEY = BLOCK_DATA_KEY
OFFER_VALIDATED_KEY = "validated"
OFFER_TIME_KEY = "offer_time"
OFFER_SORT_KEY = "offer_id"

# 30 minutes
CLEANUP_BLOCKS_TIME_THRESHOLD = 48  # Hours
CLEANUP_OFFERS_TIME_THRESHOLD = CLEANUP_BLOCKS_TIME_THRESHOLD  # Hours
SEARCH_SLEEP_TIME_THRESHOLD = 30

# cloudwatch
SEARCH_ENGINE_LOG_GROUP = "Search-Engine-Logs"

# Web endpoints
BASE_ADDRESS = "dev.blockinservice.com"
WEB_BACKEND_ERROR_ENDPOINT_URL = f"{BASE_ADDRESS}/api/errorNotification/sendAsync"
WEB_BACKEND_ENDPOINT_URL = f"{BASE_ADDRESS}/api/blockNotification/sendAsync"
WEB_BACKEND_AUTHENTICATION_URL = f"{BASE_ADDRESS}/api/externalSync/login"

# Secrets
WEB_AUTH_SECRETS = "bis-web-app-api"
WEB_API_TOKEN_KEY = "jwToken"
