from Cloud.packages.constants import constants
from Cloud.packages.sqs import sqs_manager


##############################################################################################

def dump_sqs_config():
    queues_names = [constants.SE_AUTHENTICATE_DLQ,
                    constants.SE_ACCEPTED_DLQ,
                    constants.SE_SLEEP_DLQ]

    for queue in queues_names:
        sqs_manager.remove_queue(queue)

    print(f"SQS service removed: {queues_names}")

##############################################################################################
