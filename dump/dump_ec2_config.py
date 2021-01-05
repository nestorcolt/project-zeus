from security import ec2_security_group
from constants import constants
import boto3


##############################################################################################
# Ec2 area

def dump_ec2_config():
    """
    dump the ec2 configuration
    :return:
    """
    client = boto3.client('ec2')

    # remove security groups
    ec2_security_group.delete_security_group([constants.WORKER_SECURITY_GROUP_NAME])
    launch_templates = [constants.LAUNCH_TEMPLATE_NAME]

    for template in launch_templates:
        try:
            client.delete_launch_template(LaunchTemplateName=template)
            print(f"Launch template removed: {template}")
        except Exception as e:
            print(e)

##############################################################################################
