from boot import ec2_boot, network_boot, sns_boot, sqs_boot
from Cloud.packages.storage import buckets


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

    # Create SQS DEAD LETTERS
    sqs_boot.sqs_boostrap()
    print("##############################################################################################")

    # Create SNS topics
    sns_boot.sns_boostrap()
    print("##############################################################################################")

    # End
    print("\nBootstrap process finished")


##############################################################################################

bootstrap()
