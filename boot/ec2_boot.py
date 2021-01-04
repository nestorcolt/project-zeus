from security import ec2_security_group
from Ec2 import worker_launch_template
from constants import constants
import importlib
import boto3

importlib.reload(worker_launch_template)
importlib.reload(ec2_security_group)
importlib.reload(constants)


##############################################################################################

def ec2_bootstrap(network_id=None):
    """

    Initialize the Ec2 stage configuration

    """
    # instance a ec2 client
    client = boto3.client('ec2')

    # Security group validator
    security_groups = client.describe_security_groups()["SecurityGroups"]
    sg_exist = [group for group in security_groups if group["GroupName"] == constants.WORKER_SECURITY_GROUP_NAME]

    # Template validator
    launch_templates = client.describe_launch_templates()["LaunchTemplates"]
    config_exist = [tmp for tmp in launch_templates if tmp["LaunchTemplateName"] == constants.LAUNCH_TEMPLATE_NAME]

    if not sg_exist:
        # init security group
        ec2_security_group.create_security_group(group_name=constants.WORKER_SECURITY_GROUP_NAME, vpc_id=network_id)

    if not config_exist:
        # set a waiter to wait for the security group to be crated
        waiter = client.get_waiter('security_group_exists')

        try:
            # wait for security group to be created before continue
            waiter.wait(WaiterConfig={'Delay': 30, 'MaxAttempts': 10})

            # create launch template
            worker_launch_template.create_launch_template()

        except Exception as e:
            print(e)

##############################################################################################
