from boot import ec2_boot, network_boot, sns_boot
from storage import buckets
import importlib

importlib.reload(ec2_boot)
importlib.reload(network_boot)


##############################################################################################

def bootstrap():
    # Init network configuration
    vpc_id = network_boot.network_bootstrap()
    print("##############################################################################################")

    # Init Ec2 configuration
    ec2_boot.ec2_bootstrap(network_id=vpc_id)
    print("##############################################################################################")

    # Create S3 search engine bucket
    buckets.configure_software_bucket()
    print("##############################################################################################")

    # Create SNS topics
    sns_boot.sns_boostrap()
    print("##############################################################################################")

    # End
    print("\nBootstrap process finished.")


##############################################################################################

bootstrap()
