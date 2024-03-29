from Cloud.packages.constants import constants
from Cloud.packages.sqs import sqs_manager


##############################################################################################

def dump_sqs_config():
    queues_names = [constants.SE_START_DEAD_LETTER_QUEUE,
                    constants.SE_MODIFY_DEAD_LETTER_QUEUE,
                    constants.SE_STOP_DEAD_LETTER_QUEUE,
                    constants.BLOCK_CAPTURED_DEAD_LETTER_QUEUE,
                    constants.INSTANCE_SLEEP_DEAD_LETTER_QUEUE,
                    constants.INSTANCE_AWAKE_DEAD_LETTER_QUEUE]

    for queue in queues_names:
        sqs_manager.remove_queue(queue)

    print(f"SQS service removed: {queues_names}")

##############################################################################################
