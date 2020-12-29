from botocore.exceptions import ClientError
from modules import logger
import boto3

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################

def get_security_groups(ids=None):
    ec2 = boto3.client('ec2')
    response = []

    if not ids:
        ids = []

    try:
        response = ec2.describe_security_groups(GroupIds=ids)
        log.info(response)

    except ClientError as e:
        log.exception(e)

    return response


def create_security_group(group_name="Group Name", description="Description", vpc_id=None):
    ec2 = boto3.client('ec2')

    if not vpc_id:
        response = ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName=group_name,
                                             Description=description,
                                             VpcId=vpc_id)

        security_group_id = response['GroupId']
        ec2.create_tags(Resources=[security_group_id], Tags=[{'Key': 'Name', 'Value': group_name}])
        log.info('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},

                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])

        log.info('Ingress Successfully Set %s' % data)

    except ClientError as e:
        log.exception(e)


def delete_security_group(group_id):
    # Create EC2 client
    ec2 = boto3.client('ec2')

    # Delete security group
    try:
        ec2.delete_security_group(GroupId=group_id)
        log.info('Security Group Deleted')

    except ClientError as e:
        log.exception(e)

##############################################################################################
