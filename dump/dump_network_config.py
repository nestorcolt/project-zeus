from network import network_manager
from constants import constants
import time


##############################################################################################
# Network area

def dump_network_config():
    """
    Remove the network config and leave if on a default state
    :return:
    """
    threshold = 2
    # Remove route tables
    network_manager.remove_route_tables([constants.ROUTE_TABLE_NAME])
    time.sleep(threshold)

    # Remove internet gateway
    network_manager.remove_internet_gateways([constants.INTERNET_GATEWAY_NAME])
    time.sleep(threshold)

    # Remove subnets
    network_manager.remove_subnets([constants.SUBNET_NAME])
    time.sleep(threshold)

    # Remove VPCS
    network_manager.remove_vpcs([constants.VPC_NAME])
    time.sleep(threshold)

    print(f"VPC configuration removed!")

##############################################################################################
