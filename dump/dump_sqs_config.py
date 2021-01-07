from constants import constants
from sqs import sqs_manager


##############################################################################################

def dump_sns_config():
    queues_names = [constants.SE_DEAD_LETTER_QUEUE, constants.BLOCK_CAPTURED_DEAD_LETTER_QUEUE]

    for queue in queues_names:
        sqs_manager.remove_queue(queue)

    print(f"SQS service removed: {queues_names}")

##############################################################################################
