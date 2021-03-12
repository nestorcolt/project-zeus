from Cloud.packages.constants import constants as cns
from Cloud.packages.network import network_manager
from Cloud.packages.waiters import igw_waiter
from Cloud.packages import logger
from time import sleep
import boto3

LOGGER = logger.Logger(__name__)
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
    vpc_exist = network_manager.vpc_exist_check(cns.VPC_NAME)
    vpc_waiter = client.get_waiter('vpc_available')

    if not vpc_exist:
        vpc_exist = network_manager.create_vpc(name=cns.VPC_NAME,
                                               cidr_block=cns.VPC_CIDR_BLOCK)["Vpc"]
        # wait until is created
        vpc_waiter.wait(WaiterConfig={'Delay': 30, 'MaxAttempts': 10})

    vpc_id = vpc_exist["VpcId"]

    zones = [cns.ZONE_US_EAST1A,
             cns.ZONE_US_EAST1B,
             cns.ZONE_US_EAST1C,
             cns.ZONE_US_EAST1D,
             cns.ZONE_US_EAST1E,
             cns.ZONE_US_EAST1F]

    cird_blocks = [cns.SUBNET_CIDR_BLOCK,
                   cns.SUBNET_CIDR_BLOCK_2,
                   cns.SUBNET_CIDR_BLOCK_3,
                   cns.SUBNET_CIDR_BLOCK_4,
                   cns.SUBNET_CIDR_BLOCK_5,
                   cns.SUBNET_CIDR_BLOCK_6]
    subnets = []

    for index, (zone, cird) in enumerate(zip(zones, cird_blocks)):
        # subnet validator
        subnet_name = cns.SUBNET_NAME + str(index)
        print(zone, cird, index)
        subnet_exist = network_manager.subnet_exist_check(subnet_name)
        subnet_waiter = client.get_waiter('subnet_available')

        if not subnet_exist:
            subnet_exist = network_manager.create_subnet(name=subnet_name,
                                                         vpc_id=vpc_id,
                                                         cidr_block=cird,
                                                         zone=zone)["Subnet"]
            # wait until is created
            subnet_waiter.wait(WaiterConfig={'Delay': 30, 'MaxAttempts': 10})

        subnet_id = subnet_exist["SubnetId"]
        subnets.append(subnet_id)

    # Internet gateway validator
    gateway_exist = network_manager.gateway_exist_check(cns.INTERNET_GATEWAY_NAME)

    if not gateway_exist:
        gateway_exist = network_manager.create_internet_gateway(cns.INTERNET_GATEWAY_NAME)["InternetGateway"]

    # wait for process to be created
    gateway_id = gateway_exist["InternetGatewayId"]
    igw_waiter.internet_gateway_waiter(gateway_id)

    network_manager.attach_internet_gateway(vpc_id=vpc_id,
                                            gateway_id=gateway_id)

    # Route Table Validator
    table_exist = network_manager.route_table_exist(cns.ROUTE_TABLE_NAME)

    if not table_exist:
        table_exist = network_manager.create_route_table(cns.ROUTE_TABLE_NAME, vpc_id)["RouteTable"]

    table_id = table_exist["RouteTableId"]

    # Create Routes
    network_manager.rt_create_routes(rt_id=table_id,
                                     gateway_id=gateway_id)

    for index, subnet_id in enumerate(subnets):

        if index > 1:
            # This means that only the first 2 will skip the route table and will become private subnets
            continue

        # subnet association
        network_manager.rt_associate_with_subnet(table_id, subnet_id)

    # wait a few seconds
    sleep(5)
    print("Network configuration created!")
    return vpc_id


##############################################################################################
if __name__ == '__main__':
    network_bootstrap()
