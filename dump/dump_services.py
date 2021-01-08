from dump import dump_ec2_config, dump_network_config, dump_sns_config, dump_sqs_config


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

    # Remove SNS topics
    dump_sns_config.dump_sns_config()

    # dump all Queues
    dump_sqs_config.dump_sqs_config()


##############################################################################################

dump_infrastructure()
