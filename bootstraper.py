from security import ec2_security_group
from Ec2 import worker_launch_template
from constants import constants
import importlib
import boto3

importlib.reload(worker_launch_template)
importlib.reload(ec2_security_group)
importlib.reload(constants)


# TODO Create waiters for infrastructure booting

##############################################################################################

def ec2_bootstrap():
    client = boto3.client('ec2')

    # init security group
    ec2_security_group.create_security_group(group_name=constants.WORKER_SECURITY_GROUP_NAME)

    # set a waiter to wait for the security group to be crated
    waiter = client.get_waiter('security_group_exists')

    try:
        # init launch template
        waiter.wait(WaiterConfig={'Delay': 30, 'MaxAttempts': 10})

        # create template
        worker_launch_template.create_launch_template()

    except Exception as e:
        print(e)


##############################################################################################

ec2_bootstrap()
