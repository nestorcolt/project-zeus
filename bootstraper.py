from security import ec2_security_group
from Ec2 import worker_launch_template
from constants import constants
import importlib

importlib.reload(worker_launch_template)
importlib.reload(ec2_security_group)
importlib.reload(constants)


##############################################################################################

def boot_pipeline():
    pass
    # init security group
    ec2_security_group.create_security_group(group_name=constants.WORKER_SECURITY_GROUP_NAME)

    # init launch template
    worker_launch_template.create_launch_template()


##############################################################################################

boot_pipeline()
