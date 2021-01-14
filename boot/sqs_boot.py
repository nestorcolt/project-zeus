from Cloud.packages.constants import constants
from Cloud.packages.sqs import sqs_manager
import time


##############################################################################################

def sqs_boostrap():
    print("************************\nSQS\n************************")

    # Create sqs to work as a dead letter queue for the topic of instance initializing
    sqs_manager.create_queue(name=constants.SE_START_DEAD_LETTER_QUEUE)
    sqs_manager.create_queue(name=constants.SE_MODIFY_DEAD_LETTER_QUEUE)
    sqs_manager.create_queue(name=constants.SE_STOP_DEAD_LETTER_QUEUE)

    # Create sqs to work as a dead letter queue for the captured blocks processing
    sqs_manager.create_queue(name=constants.BLOCK_CAPTURED_DEAD_LETTER_QUEUE)

    # dead letter queue for the sleep of an instance when the SE have reached max attempts
    sqs_manager.create_queue(name=constants.INSTANCE_SLEEP_DEAD_LETTER_QUEUE)

    # awake the instance dead letter queue
    sqs_manager.create_queue(name=constants.INSTANCE_AWAKE_DEAD_LETTER_QUEUE)

    time.sleep(2)
    print(f"SQS service created!")

##############################################################################################
