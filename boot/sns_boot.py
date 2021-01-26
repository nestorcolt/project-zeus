from Cloud.packages.constants import constants
from Cloud.packages.sns import sns_manager
import time


##############################################################################################

def sns_boostrap():
    print("************************\nSNS\n************************")
    # Create sns to start the user search engine instance
    sns_manager.create_topic(name=constants.AUTHENTICATE_SE_SNS_NAME)
    sns_manager.set_dead_letter_queue(queue_name=constants.SE_AUTHENTICATE_DEAD_LETTER_QUEUE,
                                      topic_name=constants.AUTHENTICATE_SE_SNS_NAME)

    # Create sns to send a message when a block has been accepted
    sns_manager.create_topic(name=constants.ACCEPTED_BLOCK_SNS_NAME)
    sns_manager.set_dead_letter_queue(queue_name=constants.BLOCK_CAPTURED_DEAD_LETTER_QUEUE,
                                      topic_name=constants.ACCEPTED_BLOCK_SNS_NAME)

    # Create sns to send a message when a block has been accepted
    sns_manager.create_topic(name=constants.INSTANCE_SLEEP_BLOCK_SNS_NAME)
    sns_manager.set_dead_letter_queue(queue_name=constants.INSTANCE_SLEEP_DEAD_LETTER_QUEUE,
                                      topic_name=constants.INSTANCE_SLEEP_BLOCK_SNS_NAME)

    # Create sns to send LOGS
    sns_manager.create_topic(name=constants.LOGS_BLOCK_SNS_NAME)
    sns_manager.set_dead_letter_queue(queue_name=constants.LOGS_DEAD_LETTER_QUEUE,
                                      topic_name=constants.LOGS_BLOCK_SNS_NAME)

    time.sleep(2)
    print(f"SNS topics created!")

##############################################################################################
