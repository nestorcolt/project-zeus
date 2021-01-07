from security import ec2_security_group
from Ec2 import launch_templates_manager
from constants import constants


##############################################################################################
# Ec2 area

def dump_ec2_config():
    """
    dump the ec2 configuration
    :return:
    """

    # Remove security groups
    ec2_security_group.delete_security_group([constants.WORKER_SECURITY_GROUP_NAME])

    # Remove launch templates
    launch_templates_to_delete = [constants.LAUNCH_TEMPLATE_NAME]
    launch_templates_manager.remove_launch_templates(launch_templates_to_delete)

    print(f"Ec2 configuration removed!")

##############################################################################################
