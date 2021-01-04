from constants import constants
import importlib
import boto3

importlib.reload(constants)


##############################################################################################

def create_vpc():
    client = boto3.client("ec2")
    response = None

    try:
        response = client.create_vpc(
            CidrBlock=constants.VPC_CIDR_BLOCK,
            InstanceTenancy='default',
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': constants.VPC_NAME
                        },
                    ]
                },
            ]
        )

        # result
        print(response)

    except Exception as e:
        print(e)

    return response


def create_subnet(vpc_id):
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
                            'Value': constants.SUBNET_NAME
                        },
                    ]
                },
            ],
            AvailabilityZone=constants.ZONE_US_EAST1,
            CidrBlock=constants.SUBNET_CIDR_BLOCK,
            VpcId=vpc_id,
            DryRun=False
        )
        # result
        print(response)

    except Exception as e:
        print(e)

    return response


def create_internet_gateway():
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
                            'Value': constants.INTERNET_GATEWAY_NAME,
                        },
                    ]
                },
            ],
            DryRun=False
        )
        # result
        print(response)

    except Exception as e:
        print(e)

    return response


def attach_internet_gateway(vpc_id, gateway_id):
    client = boto3.client("ec2")
    response = client.attach_internet_gateway(
        DryRun=False,
        InternetGatewayId=gateway_id,
        VpcId=vpc_id
    )
    return response


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
        print(response)

    except Exception as e:
        print(e)

    return response


def rt_create_routes(rt_id, gateway_id, cidr_route="0.0.0.0/0"):
    ec2 = boto3.resource('ec2')
    route_table = ec2.RouteTable(rt_id)
    route_table.create_route(DestinationCidrBlock=cidr_route, GatewayId=gateway_id)


def rt_associate_with_subnet(rt_id, subnet_id):
    ec2 = boto3.resource('ec2')
    route_table = ec2.RouteTable(rt_id)
    route_table_association = route_table.associate_with_subnet(
        DryRun=False,
        SubnetId=subnet_id,
    )
    return route_table_association


##############################################################################################

# create_vpc()
# create_subnet("vpc-0d42e68f7c8028e3d")
# create_internet_gateway()
# attach_internet_gateway("vpc-0d42e68f7c8028e3d","igw-0ad477537824bb0fa")
# create_route_table(constants.ROUTE_TABLE_NAME, "vpc-0d42e68f7c8028e3d")
# rt_create_routes("rtb-0efaf0fbf8a585d38", "igw-0ad477537824bb0fa")
# rt_associate_with_subnet("rtb-0efaf0fbf8a585d38", "subnet-0a83e9343dbb45225")
