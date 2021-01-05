from boot import ec2_boot, network_boot
from storage import buckets
import importlib

importlib.reload(ec2_boot)
importlib.reload(network_boot)


##############################################################################################

def bootstrap():
    # Init network configuration
    vpc_id = network_boot.network_bootstrap()

    # Init Ec2 configuration
    ec2_boot.ec2_bootstrap(network_id=vpc_id)

    # Create S3 search engine bucket
    buckets.configure_software_bucket()

    # End
    print("\nBootstrap process finished.")


##############################################################################################

bootstrap()
