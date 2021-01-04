from security import ec2_security_group
from Ec2 import worker_launch_template
from network import network_manager
from constants import constants
import importlib
import boto3

importlib.reload(worker_launch_template)
importlib.reload(ec2_security_group)
importlib.reload(constants)
importlib.reload(network_manager)


##############################################################################################

def network_bootstrap():
    """

    Initialize the network configuration

    """
    # instance a ec2 client
    client = boto3.client('ec2')

    # create_vpc()
    # create_subnet("vpc-0d42e68f7c8028e3d")
    # create_internet_gateway()
    # attach_internet_gateway("vpc-0d42e68f7c8028e3d","igw-0ad477537824bb0fa")
    # create_route_table(constants.ROUTE_TABLE_NAME, "vpc-0d42e68f7c8028e3d")
    # rt_create_routes("rtb-0efaf0fbf8a585d38", "igw-0ad477537824bb0fa")
    # rt_associate_with_subnet("rtb-0efaf0fbf8a585d38", "subnet-0a83e9343dbb45225")

##############################################################################################
