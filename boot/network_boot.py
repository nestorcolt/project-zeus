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
    vpcs = client.describe_vpcs()["Vpcs"]
    vpc_exist = [vpc for vpc in vpcs if vpc["Tags"][0]["Value"] == constants.VPC_NAME]

    if not vpc_exist:
        vpc_exist = network_manager.create_vpc(name=constants.VPC_NAME,
                                               cidr_block=constants.VPC_CIDR_BLOCK)

    vpc_id = vpc_exist[0]["VpcId"]

    # subnet validator
    subnets = client.describe_subnets()["Subnets"]
    subnet_exist = False

    for subnet in subnets:
        tags = subnet.get("Tags")

        if not tags:
            continue

        if tags[0]["Value"] == constants.SUBNET_NAME:
            subnet_exist = subnet
            break

    if not subnet_exist:
        network_manager.create_subnet(name=constants.SUBNET_NAME,
                                      vpc_id=vpc_id,
                                      cidr_block=constants.SUBNET_CIDR_BLOCK,
                                      zone=constants.ZONE_US_EAST1)

    subnet_id = subnet_exist["SubnetId"]

    # Internet gateway validator
    gateways = client.describe_internet_gateways()["InternetGateways"]
    gateway_exist = False

    for gate in gateways:
        tags = gate.get("Tags")

        if not tags:
            continue

        if tags[0]["Value"] == constants.INTERNET_GATEWAY_NAME:
            gateway_exist = gate
            break

    if not gateway_exist:
        gateway_exist = network_manager.create_internet_gateway(constants.INTERNET_GATEWAY_NAME)

    gateway_id = gateway_exist["InternetGatewayId"]

    if not gateway_exist["Attachments"]:
        network_manager.attach_internet_gateway(vpc_id=vpc_id,
                                                gateway_id=gateway_id)

    # Route Table Validator
    route_tables = client.describe_route_tables()["RouteTables"]
    table_exist = False

    for table in route_tables:
        tags = table.get("Tags")

        if not tags:
            continue

        if tags[0]["Value"] == constants.ROUTE_TABLE_NAME:
            table_exist = table
            break

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
