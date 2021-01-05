from dump import dump_ec2_config, dump_network_config
from constants import constants
from storage import buckets
import importlib

importlib.reload(dump_ec2_config)


##############################################################################################

def dump_infrastructure():
    """
    Dump all the configuration created by code and restore the state of AWS account
    to its default previous to code bootloader
    """
    # Dump the Ec2 service configuration
    dump_ec2_config.dump_ec2_config()

    # Dump network
    dump_network_config.dump_network_config()

    # Remove buckets
    my_buckets = [constants.SEARCH_ENGINE_BUCKET_NAME]

    for itm in my_buckets:
        buckets.delete_bucket(itm)


##############################################################################################

dump_infrastructure()
