from dump import dump_ec2_config
import importlib

importlib.reload(dump_ec2_config)


##############################################################################################

def dump_infrastructure():
    """
    Dump all the configuration created by code and restore the state of AWS account
    to its default previous to code bootloader
    """
    # dump the Ec2 service configuration
    dump_ec2_config.dump_ec2_config()


##############################################################################################

dump_infrastructure()
