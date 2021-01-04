"""

    Constants for Ec2 usage

"""
# Zones
ZONE_US_EAST1 = "us-east-1b"


# Launch Template Ec2
LAUNCH_TEMPLATE_NAME = "Worker-Template"
LAUNCH_TEMPLATE_VERSION = "1"
AMI_ID = "ami-0550151dfa2d7ecc3"
KEY_PAIR_NAME = "worker-pem-file"
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

