from Cloud.boot import ec2_boot, network_boot, sns_boot, sqs_boot, iam_boot
from Cloud.packages.storage import buckets


##############################################################################################

def bootstrap():
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
