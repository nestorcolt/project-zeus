from network import network_manager
from constants import constants
from waiters import igw_waiter
from modules import logger
from time import sleep
import boto3

LOGGER = logger.Logger("Network Boot")
LOGGER.set_file_handle()
log = LOGGER.logger


##############################################################################################

def network_bootstrap():
    """

    Initialize the network configuration

    """
    print("************************\nVPC\n************************")
    # instance a ec2 client
    client = boto3.client('ec2')

    # VPC validator
    vpc_exist = network_manager.vpc_exist_check(constants.VPC_NAME)
    vpc_waiter = client.get_waiter('vpc_available')

    if not vpc_exist:
        vpc_exist = network_manager.create_vpc(name=constants.VPC_NAME,
                                               cidr_block=constants.VPC_CIDR_BLOCK)["Vpc"]
        # wait until is created
        vpc_waiter.wait(WaiterConfig={'Delay': 30, 'MaxAttempts': 10})

    vpc_id = vpc_exist["VpcId"]

    # subnet validator
    subnet_exist = network_manager.subnet_exist_check(constants.SUBNET_NAME)
    subnet_waiter = client.get_waiter('subnet_available')

    if not subnet_exist:
        subnet_exist = network_manager.create_subnet(name=constants.SUBNET_NAME,
                                                     vpc_id=vpc_id,
                                                     cidr_block=constants.SUBNET_CIDR_BLOCK,
                                                     zone=constants.ZONE_US_EAST1)["Subnet"]
        # wait until is created
        subnet_waiter.wait(WaiterConfig={'Delay': 30, 'MaxAttempts': 10})

    subnet_id = subnet_exist["SubnetId"]

    # Internet gateway validator
    gateway_exist = network_manager.gateway_exist_check(constants.INTERNET_GATEWAY_NAME)

    if not gateway_exist:
        gateway_exist = network_manager.create_internet_gateway(constants.INTERNET_GATEWAY_NAME)["InternetGateway"]

    # wait for process to be created
    gateway_id = gateway_exist["InternetGatewayId"]
    igw_waiter.internet_gateway_waiter(gateway_id)

    network_manager.attach_internet_gateway(vpc_id=vpc_id,
                                            gateway_id=gateway_id)

    # Route Table Validator
    table_exist = network_manager.route_table_exist(constants.ROUTE_TABLE_NAME)

    if not table_exist:
        table_exist = network_manager.create_route_table(constants.ROUTE_TABLE_NAME, vpc_id)["RouteTable"]

    table_id = table_exist["RouteTableId"]

    # Create Routes
    network_manager.rt_create_routes(rt_id=table_id,
                                     gateway_id=gateway_id)
    # subnet association
    network_manager.rt_associate_with_subnet(table_id, subnet_id)

    # wait a few seconds
    sleep(2)

    print("Network configuration created!")
    return vpc_id

##############################################################################################
