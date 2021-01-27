from Cloud.packages.constants import constants
from Cloud.packages.sns import sns_manager


##############################################################################################

def dump_sns_config():
    topic_names = [constants.SE_AUTHENTICATE_TOPIC,
                   constants.SE_ACCEPTED_TOPIC,
                   constants.SE_SLEEP_TOPIC]

    queues_names = [constants.SE_AUTHENTICATE_DLQ,
                    constants.SE_ACCEPTED_DLQ,
                    constants.SE_SLEEP_DLQ]

    # Delete all subscriptions
    sns_manager.delete_subscriptions(queues_names)

    for topic in topic_names:
        sns_manager.delete_topic(topic)

    print(f"SNS topics removed: {topic_names}")

##############################################################################################
