from Cloud.packages.constants import constants
from Cloud.packages.sqs import sqs_manager
import time


##############################################################################################

def sqs_boostrap():
    print("************************\nSQS\n************************")

    # Create sqs to work as a dead letter queue for the topic of instance initializing
    sqs_manager.create_queue(name=constants.SE_START_DLQ)
    sqs_manager.create_queue(name=constants.SE_AUTHENTICATE_DLQ)

    # Create sqs to work as a dead letter queue for the captured blocks processing
    sqs_manager.create_queue(name=constants.SE_ACCEPTED_DLQ)
    sqs_manager.create_queue(name=constants.SE_SLEEP_DLQ)
    sqs_manager.create_queue(name=constants.SE_ERROR_DLQ)
    sqs_manager.create_queue(name=constants.SE_LOGS_DLQ)

    time.sleep(2)
    print(f"SQS service created!")

##############################################################################################
