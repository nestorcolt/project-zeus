from constants import constants
from sns import sns_manager
import importlib
import boto3

importlib.reload(sns_manager)
importlib.reload(constants)


def sns_boostrap():
    # Create sns to start the user search engine instance
    sns_manager.create_topic(name=constants.START_SE_SNS_NAME)

    # Create sns to stop the user search engine instance
    sns_manager.create_topic(name=constants.STOP_SE_SNS_NAME)

    # Create sns to pause the user search engine instance
    sns_manager.create_topic(name=constants.PAUSE_SE_SNS_NAME)

    # Create sns to send a message when a block has been accepted
    sns_manager.create_topic(name=constants.ACCEPTED_BLOCK_SNS_NAME)

    print(f"SNS topics Created!")
