from constants import constants
from sqs import sqs_manager


##############################################################################################

def sns_boostrap():
    print("************************\nSQS\n************************")

    # Create sqs to work as a dead letter queue for the topic of instance initializing
    sqs_manager.get_queue_by_name(name=constants.SE_DEAD_LETTER_QUEUE)

    # Create sqs to work as a dead letter queue for the captured blocks processing
    sqs_manager.get_queue_by_name(name=constants.BLOCK_CAPTURED_DEAD_LETTER_QUEUE)

    print(f"SQS service created!")

##############################################################################################
