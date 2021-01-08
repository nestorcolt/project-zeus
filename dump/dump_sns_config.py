from constants import constants
from sns import sns_manager


##############################################################################################

def dump_sns_config():
    topic_names = [constants.STOP_SE_SNS_NAME,
                   constants.START_SE_SNS_NAME,
                   constants.PAUSE_SE_SNS_NAME,
                   constants.ACCEPTED_BLOCK_SNS_NAME]

    for topic in topic_names:
        sns_manager.delete_topic(topic)

    print(f"SNS topics removed: {topic_names}")


##############################################################################################

dump_sns_config()
