from Cloud.packages.constants import constants
from Cloud.packages.sqs import sqs_manager


##############################################################################################

def sqs_boostrap():
    print("************************\nSQS\n************************")

    # Create sqs to work as a dead letter queue for the topic of instance initializing
    sqs_manager.create_queue(name=constants.SE_START_DEAD_LETTER_QUEUE)
    sqs_manager.create_queue(name=constants.SE_PAUSE_DEAD_LETTER_QUEUE)
    sqs_manager.create_queue(name=constants.SE_STOP_DEAD_LETTER_QUEUE)

    # Create sqs to work as a dead letter queue for the captured blocks processing
    sqs_manager.create_queue(name=constants.BLOCK_CAPTURED_DEAD_LETTER_QUEUE)

    print(f"SQS service created!")

##############################################################################################
