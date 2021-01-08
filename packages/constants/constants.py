"""

    Constants

"""

import inspect
import os

# Global vars
CURRENT_FRAME = inspect.getfile(inspect.currentframe())
ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FRAME)))
VERSION = "1.0.2"

# Logs
LOG_FILE_NAME = "bis_logs.txt"

# Zones
ZONE_US_EAST1 = "us-east-1b"

# Launch Template Ec2
AMI_ID = "ami-0550151dfa2d7ecc3"
LAUNCH_TEMPLATE_NAME = "Worker-Template"
KEY_PAIR_NAME = "worker-pem-file"
LAUNCH_TEMPLATE_VERSION = "1"
INSTANCE_TYPE = "t3a.micro"

# Security Groups Ec2
WORKER_SECURITY_GROUP_NAME = "Worker-SG"

# VPC
VPC_NAME = "BIS-VPC"
VPC_CIDR_BLOCK = "10.0.0.0/16"

# Subnet
SUBNET_NAME = "BIS-Subnet"
SUBNET_CIDR_BLOCK = "10.0.1.0/24"
INTERNET_GATEWAY_NAME = "BIS-Int-Gateway"
ROUTE_TABLE_NAME = "BIS-Route-Table"

# Buckets
SEARCH_ENGINE_BUCKET_NAME = "bis-se-s3"
LAMBDA_BUCKET_NAME = "bis-serverless-s3"

# SNS
START_SE_SNS_NAME = "SE-START-SERVICE"
STOP_SE_SNS_NAME = "SE-STOP-SERVICE"
PAUSE_SE_SNS_NAME = "SE-PAUSE-SERVICE"
ACCEPTED_BLOCK_SNS_NAME = "SE-ACCEPTED-BLOCK-SERVICE"

# SQS
SE_START_DEAD_LETTER_QUEUE = "SE-START-DLQ"
SE_PAUSE_DEAD_LETTER_QUEUE = "SE-PAUSE-DLQ"
SE_STOP_DEAD_LETTER_QUEUE = "SE-STOP-DLQ"
BLOCK_CAPTURED_DEAD_LETTER_QUEUE = "CB-DLQ"
