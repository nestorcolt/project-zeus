from Cloud.packages.security import ec2_security_group
from Cloud.packages.Ec2 import launch_templates_manager
from Cloud.packages.constants import constants
from Cloud.packages import logger
import boto3

LOGGER = logger.Logger("Ec2 Boot")
log = LOGGER.logger


##############################################################################################

def ec2_bootstrap(network_id=None):
    """

    Initialize the Ec2 stage configuration

    """
    print("************************\nEc2\n************************")
    # instance a ec2 client
    client = boto3.client('ec2')

    # Security group validator
    security_groups = client.describe_security_groups()["SecurityGroups"]
    sg_exist = [group for group in security_groups if group["GroupName"] == constants.WORKER_SECURITY_GROUP_NAME]
    web_sg_exist = [group for group in security_groups if group["GroupName"] == constants.WEB_SECURITY_GROUP_NAME]

    # Template validator
    launch_templates = client.describe_launch_templates()["LaunchTemplates"]
    config_exist = [tmp for tmp in launch_templates if
                    tmp["LaunchTemplateName"] == constants.WORKER_LAUNCH_TEMPLATE_NAME]

    if not sg_exist:
        # init security group
        ec2_security_group.create_security_group(group_name=constants.WORKER_SECURITY_GROUP_NAME, vpc_id=network_id)
        print("Worker Security group created!")

    if not web_sg_exist:
        # init security group
        ec2_security_group.create_security_group(group_name=constants.WEB_SECURITY_GROUP_NAME, vpc_id=network_id)
        print("Web Security group created!")

    if not config_exist:
        # set a waiter to wait for the security group to be crated
        waiter = client.get_waiter('security_group_exists')

        try:
            # wait for security group to be created before continue
            waiter.wait(WaiterConfig={'Delay': 30, 'MaxAttempts': 10})

            # create launch template
            launch_templates_manager.create_worker_launch_template()
            print("Launch templates created!")

        except Exception as e:
            log.exception(e)

##############################################################################################
