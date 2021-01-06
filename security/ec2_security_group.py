from botocore.exceptions import ClientError
from modules import logger
import boto3

LOGGER = logger.Logger("Ec2 Security")
log = LOGGER.logger


##############################################################################################

def get_security_groups(ids=None):
    ec2 = boto3.client('ec2')
    response = []

    if not ids:
        ids = []

    try:
        response = ec2.describe_security_groups(GroupIds=ids)

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


def delete_security_group(my_groups):
    client = boto3.client('ec2')
    ec2 = boto3.resource('ec2')

    security_groups = client.describe_security_groups()["SecurityGroups"]

    for group in security_groups:
        name = group["GroupName"]

        if name not in my_groups:
            continue

        group_id = group["GroupId"]
        sg = ec2.SecurityGroup(group_id)

        try:
            sg.delete()
            log.info('Security Group Deleted')

        except Exception as e:
            log.exception(e)

##############################################################################################
