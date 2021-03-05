from Cloud.packages.constants import constants
from Cloud.packages.sns import sns_manager
import time


##############################################################################################

def sns_boostrap():
    print("************************\nSNS\n************************")
    # Create sns to start the user search engine instance
    sns_manager.create_topic(name=constants.SE_START_TOPIC)
    sns_manager.create_topic(name=constants.SE_STOP_TOPIC)
    sns_manager.create_topic(name=constants.SE_AUTHENTICATE_TOPIC)

    # Create sns to send a message when a block has been accepted
    sns_manager.create_topic(name=constants.SE_ACCEPTED_TOPIC)

    # Create sns to send a message when a block has been accepted
    sns_manager.create_topic(name=constants.SE_SLEEP_TOPIC)

    # Create sns to send LOGS
    sns_manager.create_topic(name=constants.SE_LOGS_TOPIC)

    # Create sns to send LOGS
    sns_manager.create_topic(name=constants.SE_ERROR_TOPIC)

    sns_manager.create_topic(name=constants.SE_OFFERS_TOPIC)

    time.sleep(2)
    print(f"SNS topics created!")

##############################################################################################
