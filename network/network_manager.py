from constants import constants
from modules import logger
import importlib
import boto3

importlib.reload(constants)

LOGGER = logger.Logger("Virtual Private Cloud")
LOGGER.set_file_handle()
log = LOGGER.logger

##############################################################################################
"""

VPC

"""


def create_vpc(name, cidr_block, tenancy="default"):
    client = boto3.client("ec2")
    response = None

    try:
        response = client.create_vpc(
            CidrBlock=cidr_block,
            InstanceTenancy=tenancy,
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name
                        },
                    ]
                },
            ]
        )

        # result
        log.debug(response)

    except Exception as e:
        log.exception(e)

    return response


def vpc_exist_check(name):
    client = boto3.client('ec2')
    vpcs = client.describe_vpcs()["Vpcs"]
    vpc_exist = [vpc for vpc in vpcs if vpc["Tags"][0]["Value"] == name]

    if vpc_exist:
        return vpc_exist[0]


def remove_vpcs(vpc_list):
    # Remove route tables
    client = boto3.client('ec2')
    ec2 = boto3.resource('ec2')

    vpcs = client.describe_vpcs(Filters=[{"Name": "tag:Name", "Values": vpc_list}])

    for vpc in vpcs["Vpcs"]:
        vpc_id = vpc["VpcId"]
        vpc_object = ec2.Vpc(vpc_id)
        vpc_object.delete()

    log.info(f"Vpc's Removed: {vpc_list}")


##############################################################################################
"""

Subnet

"""


def create_subnet(name, vpc_id, cidr_block, zone):
    client = boto3.client("ec2")
    response = None

    try:
        response = client.create_subnet(
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name
                        },
                    ]
                },
            ],
            AvailabilityZone=zone,
            CidrBlock=cidr_block,
            VpcId=vpc_id,
            DryRun=False
        )
        # result
        log.debug(response)

    except Exception as e:
        log.exception(e)

    return response


def subnet_exist_check(name):
    client = boto3.client("ec2")
    subnets = client.describe_subnets()["Subnets"]
    subnet_exist = False

    for subnet in subnets:
        tags = subnet.get("Tags")

        if not tags:
            continue

        if tags[0]["Value"] == name:
            subnet_exist = subnet
            break

    return subnet_exist


def remove_subnets(subnet_list):
    # Remove route tables
    client = boto3.client('ec2')
    ec2 = boto3.resource('ec2')

    subnets = client.describe_subnets(Filters=[{"Name": "tag:Name", "Values": subnet_list}])

    for subnet in subnets["Subnets"]:
        subnet_id = subnet["SubnetId"]
        subnet_object = ec2.Subnet(subnet_id)
        subnet_object.delete()

    log.info(f"Subnets Removed: {subnet_list}")


##############################################################################################
"""

Internet gateway

"""


def create_internet_gateway(name):
    client = boto3.client("ec2")
    response = None

    try:
        response = client.create_internet_gateway(
            TagSpecifications=[
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name,
                        },
                    ]
                },
            ],
            DryRun=False
        )
        # result
        log.debug(response)

    except Exception as e:
        log.warning(e)

    return response


def gateway_exist_check(name):
    client = boto3.client("ec2")
    gateways = client.describe_internet_gateways()["InternetGateways"]
    gateway_exist = False

    for gate in gateways:
        tags = gate.get("Tags")

        if not tags:
            continue

        if tags[0]["Value"] == name:
            gateway_exist = gate
            break

    return gateway_exist


def attach_internet_gateway(vpc_id, gateway_id):
    client = boto3.client("ec2")
    resource = boto3.resource('ec2')
    iga = resource.InternetGateway(gateway_id)
    attachment = [itm for itm in iga.attachments if itm["VpcId"] == vpc_id]

    if attachment:
        return

    response = client.attach_internet_gateway(
        DryRun=False,
        InternetGatewayId=gateway_id,
        VpcId=vpc_id
    )
    return response


def remove_internet_gateways(gate_away_names):
    # Remove route tables
    client = boto3.client('ec2')
    ec2 = boto3.resource('ec2')

    gates = client.describe_internet_gateways(Filters=[{"Name": "tag:Name", "Values": gate_away_names}])

    for gate in gates["InternetGateways"]:
        gate_id = gate["InternetGatewayId"]
        gateway = ec2.InternetGateway(gate_id)
        attachments = gateway.attachments

        if attachments:
            _id = attachments[0].get("VpcId")
            gateway.detach_from_vpc(VpcId=_id)

        gateway.delete()

    log.info(f"Internet Gateways Removed: {gate_away_names}")


##############################################################################################
"""

    Route tables

"""


def create_route_table(name, vpc_id):
    client = boto3.client("ec2")
    response = None

    try:
        response = client.create_route_table(
            DryRun=False,
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'route-table',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name
                        },
                    ]
                },
            ]
        )
        # result
        log.debug(response)

    except Exception as e:
        log.exception(e)

    return response


def route_table_exist(name):
    client = boto3.client("ec2")
    route_tables = client.describe_route_tables()["RouteTables"]
    table_exist = False

    for table in route_tables:
        tags = table.get("Tags")

        if not tags:
            continue

        if tags[0]["Value"] == name:
            table_exist = table
            break

    return table_exist


def rt_create_routes(rt_id, gateway_id, cidr_route="0.0.0.0/0"):
    ec2 = boto3.resource('ec2')
    route_table = ec2.RouteTable(rt_id)

    for table in route_table.routes_attribute:
        block = table.get("DestinationCidrBlock")
        gateway = table.get("GatewayId")

        if block == cidr_route and gateway == gateway_id:
            return

        elif block == cidr_route and gateway != gateway_id:
            ec2.delete_route(DestinationCidrBlock=cidr_route, RouteTableId=rt_id)
            return

    route_table.create_route(DestinationCidrBlock=cidr_route, GatewayId=gateway_id)


def rt_associate_with_subnet(rt_id, subnet_id):
    ec2 = boto3.resource('ec2')
    route_table = ec2.RouteTable(rt_id)
    route_table_association = route_table.associate_with_subnet(
        DryRun=False,
        SubnetId=subnet_id,
    )
    return route_table_association


def remove_route_tables(table_list):
    # Remove route tables
    client = boto3.client('ec2')
    ec2 = boto3.resource('ec2')

    tables = client.describe_route_tables(Filters=[{"Name": "tag:Name", "Values": table_list}])

    for table in tables["RouteTables"]:
        table_id = table["RouteTableId"]
        route_table = ec2.RouteTable(table_id)

        associations = route_table.associations

        for aso in associations:
            aso.delete()

        route_table.delete()

    log.info(f"Route Tables Removed: {table_list}")

##############################################################################################
