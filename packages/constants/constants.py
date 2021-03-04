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

# Launch Template Ec2
AMI_ID = "ami-06d46e936b077fb88"
AMI_NAME = "ami-worker-ubuntu"

WORKER_LAUNCH_TEMPLATE_NAME = "Worker-Template"
KEY_PAIR_NAME = "worker-pem-file"
INSTANCE_TYPE = "t3a.micro"

"""

    Network configuration

"""

# Security Groups Ec2
WORKER_SECURITY_GROUP_NAME = "Worker-SG"
WEB_SECURITY_GROUP_NAME = "WEB-APP-SG"
DB_SECURITY_GROUP_NAME = "WEB-DB-SG"

# VPC
VPC_NAME = "BIS-VPC"
VPC_CIDR_BLOCK = "10.0.0.0/16"

# Subnet 001
INTERNET_GATEWAY_NAME = "BIS-Int-Gateway-00"
ROUTE_TABLE_NAME = "BIS-Route-Table-00"
SUBNET_CIDR_BLOCK = "10.0.1.0/24"
SUBNET_NAME = "BIS-Subnet-00"
ZONE_US_EAST1A = "us-east-1a"

# Subnet 002
SUBNET_CIDR_BLOCK_2 = "10.0.2.0/24"
ZONE_US_EAST1B = "us-east-1b"

##############################################################################################

# Buckets
LAMBDA_BUCKET_NAME = "bis-serverless-s3"

# SNS
SE_AUTHENTICATE_TOPIC = "SE-AUTHENTICATE-TOPIC"
SE_ACCEPTED_TOPIC = "SE-ACCEPTED-TOPIC"
SE_START_TOPIC = "SE-START-TOPIC"
SE_STOP_TOPIC = "SE-STOP-TOPIC"
SE_OFFERS_TOPIC = "SE-OFFERS-TOPIC"
SE_SLEEP_TOPIC = "SE-SLEEP-TOPIC"
SE_ERROR_TOPIC = "SE-ERROR-TOPIC"
SE_LOGS_TOPIC = "SE-LOGS-TOPIC"

# SQS
SE_AUTHENTICATE_DLQ = "SE-AUTHENTICATE-DLQ"
SE_ACCEPTED_DLQ = "SE-ACCEPTED-DLQ"
SE_OFFERS_DLQ = "SE-OFFERS-DLQ"
SE_START_DLQ = "SE-START-DLQ"
SE_STOP_DLQ = "SE-STOP-DLQ"
SE_ERROR_DLQ = "SE-ERROR-DLQ"
SE_SLEEP_DLQ = "SE-SLEEP-DLQ"
SE_LOGS_DLQ = "SE-LOGS-DLQ"
SE_ON_PROCESS = "SeOnProcessQueue"
SE_START_QUEUE = "GetUserBlocksQueue"

# IAM
EC2_WORKER_IAM_INSTANCE_PROFILE = "ec2-worker-instance-profile"
EC2_TO_SNS_AND_S3_POLICY = "S3AndSnsEc2Policy"
EC2_WORKER_IAM_ROLE = "ec2-worker-iam-role"

# dynamo DB
STATISTICS_TABLE_NAME = "Statistics"
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
TTL_ATTR_KEY = "ttl_attr"
OFFER_SORT_KEY = "offer_id"
STS_OFFER_KEY = "offers"
STS_ACCEPTED_KEY = "accepted"
STS_VALIDATED_KEY = "validated"

# 30 minutes
CLEANUP_BLOCKS_TIME_THRESHOLD = 24  # Hours
CLEANUP_OFFERS_TIME_THRESHOLD = CLEANUP_BLOCKS_TIME_THRESHOLD  # Hours
SEARCH_SLEEP_TIME_THRESHOLD = 30

# cloudwatch
SEARCH_ENGINE_LOG_GROUP = "Search-Engine-Logs"

# Web endpoints
BASE_ADDRESS = "https://dev.blockinservice.com"
WEB_BACKEND_ERROR_ENDPOINT_URL = f"{BASE_ADDRESS}/api/errorNotification/sendAsync"
WEB_BACKEND_ENDPOINT_URL = f"{BASE_ADDRESS}/api/blockNotification/sendAsync"
WEB_BACKEND_AUTHENTICATION_URL = f"{BASE_ADDRESS}/api/externalSync/login"

# Secrets
WEB_AUTH_TOKEN_SECRET = "bis-web-app-token"
WEB_AUTH_SECRETS = "bis-web-app-api"
WEB_API_TOKEN_KEY = "jwToken"
