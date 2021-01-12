from Cloud.packages.iam import policies
from Cloud.packages import logger
import boto3
import json

LOGGER = logger.Logger("IAM")
log = LOGGER.logger


##############################################################################################

def create_aim_policy(policy_name, policy_document, description):
    # Create IAM client
    client = boto3.client('iam')

    try:
        response = client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document),
            Description=description
        )
        log.info(response)
    except Exception as e:
        log.error(e)


def create_aim_role(role_name, description, policy_document):
    # Create IAM client
    client = boto3.client('iam')

    try:
        response = client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=policy_document,
            Description=description
        )
        log.info(response)
    except Exception as e:
        log.error(e)


def attach_role_policy(role_name, policy_arn):
    # Create IAM client
    client = boto3.client('iam')
    try:
        response = client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        log.info(response)
    except Exception as e:
        log.error(e)


def get_policy_arn(name):
    pass


get_policy_arn("")