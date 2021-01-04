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

    # VPC validator
    vpc_exist = network_manager.vpc_exist_check(constants.VPC_NAME)

    if not vpc_exist:
        vpc_exist = network_manager.create_vpc(name=constants.VPC_NAME,
                                               cidr_block=constants.VPC_CIDR_BLOCK)

    vpc_id = vpc_exist[0]["VpcId"]

    # subnet validator
    subnet_exist = network_manager.subnet_exist_check(constants.SUBNET_NAME)

    if not subnet_exist:
        network_manager.create_subnet(name=constants.SUBNET_NAME,
                                      vpc_id=vpc_id,
                                      cidr_block=constants.SUBNET_CIDR_BLOCK,
                                      zone=constants.ZONE_US_EAST1)

    subnet_id = subnet_exist["SubnetId"]

    # Internet gateway validator
    gateway_exist = network_manager.gateway_exist_check(constants.INTERNET_GATEWAY_NAME)

    if not gateway_exist:
        gateway_exist = network_manager.create_internet_gateway(constants.INTERNET_GATEWAY_NAME)

    gateway_id = gateway_exist["InternetGatewayId"]

    if not gateway_exist["Attachments"]:
        network_manager.attach_internet_gateway(vpc_id=vpc_id,
                                                gateway_id=gateway_id)

    # Route Table Validator
    table_exist = network_manager.route_table_exist(constants.ROUTE_TABLE_NAME)

    if not table_exist:
        table_exist = network_manager.create_route_table(constants.ROUTE_TABLE_NAME, vpc_id)

    table_id = table_exist["RouteTableId"]

    # Create Routes
    network_manager.rt_create_routes(rt_id=table_id,
                                     gateway_id=gateway_id)
    # subnet association
    network_manager.rt_associate_with_subnet(table_id, subnet_id)


##############################################################################################

network_bootstrap()
