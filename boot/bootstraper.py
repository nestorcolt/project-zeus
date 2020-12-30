from boot import ec2_boot
import importlib

importlib.reload(ec2_boot)


##############################################################################################

def bootstrap():
    # Init Ec2 configuration
    ec2_boot.ec2_bootstrap()


##############################################################################################

bootstrap()
