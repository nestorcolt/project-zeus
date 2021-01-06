from modules import logger
import boto3

LOGGER = logger.Logger("SNS")
LOGGER.set_stream_handle()
log = LOGGER.logger


##############################################################################################

def get_topic_by_name(topic_name):
    client = boto3.client('sns')
    topics = client.list_topics()
    check = [itm for itm in topics["Topics"] if itm["TopicArn"].split(":")[-1] == topic_name]
    return check


def create_topic(name):
    client = boto3.client('sns')

    if get_topic_by_name(name):
        return

    try:
        response = client.create_topic(
            Name=name,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': name
                },
            ]
        )

        log.debug(response)

    except Exception as e:
        log.exception(e)


def delete_topic(name):
    client = boto3.client('sns')
    topic = get_topic_by_name(name)

    if not topic:
        return

    try:
        response = client.delete_topic(
            TopicArn=topic[0]["TopicArn"]
        )

        log.debug(response)

    except Exception as e:
        log.exception(e)


def create_subscription(name, protocol, endpoint_id):
    client = boto3.client('sns')
    topic = get_topic_by_name(name)

    if not topic:
        log.debug("No topic found to add subscription")
        return

    response = None

    try:
        response = client.subscribe(
            TopicArn=topic[0]["TopicArn"],
            Protocol=protocol,
            Endpoint=endpoint_id,
            ReturnSubscriptionArn=True
        )
        log.debug(response)

    except Exception as e:
        log.exception(e)

    return response


def delete_subscriptions(endpoint_id=None):
    client = boto3.client('sns')
    subscriptions = client.list_subscriptions()

    for sub in subscriptions["Subscriptions"]:
        arn = sub["SubscriptionArn"]

        if endpoint_id:
            endpoint_arn = sub["Endpoint"]
            if endpoint_arn == endpoint_id:
                client.unsubscribe(SubscriptionArn=arn)
        else:
            client.unsubscribe(SubscriptionArn=arn)

##############################################################################################
