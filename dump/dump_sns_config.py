from Cloud.packages.constants import constants
from Cloud.packages.sns import sns_manager


##############################################################################################

def dump_sns_config():
    topic_names = [constants.AUTHENTICATE_SE_SNS_NAME,
                   constants.ACCEPTED_BLOCK_SNS_NAME,
                   constants.INSTANCE_SLEEP_BLOCK_SNS_NAME]

    queues_names = [constants.SE_AUTHENTICATE_DEAD_LETTER_QUEUE,
                    constants.BLOCK_CAPTURED_DEAD_LETTER_QUEUE,
                    constants.INSTANCE_SLEEP_DEAD_LETTER_QUEUE]

    # Delete all subscriptions
    sns_manager.delete_subscriptions(queues_names)

    for topic in topic_names:
        sns_manager.delete_topic(topic)

    print(f"SNS topics removed: {topic_names}")

##############################################################################################
