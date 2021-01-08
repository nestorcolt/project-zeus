from packages.sqs import sqs_manager
from packages import logger
import boto3
import json

LOGGER = logger.Logger("SNS")
LOGGER.set_file_handle()
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
        )["SubscriptionArn"]
        log.debug(response)

    except Exception as e:
        log.exception(e)

    return response


def get_subscription_by_name(name):
    client = boto3.client('sns')
    subscriptions = client.list_subscriptions()
    subscription = [itm for itm in subscriptions if name in itm["SubscriptionArn"].split(":")]

    if subscription:
        return {name: subscription[0]}


def delete_subscriptions(subscriptions_to_delete):
    resource = boto3.resource('sns')
    subscriptions = list(resource.subscriptions.all())

    for itm in subscriptions:
        endpoint = itm.attributes["Endpoint"]
        endpoint_name = endpoint.split(":")[-1]

        if endpoint_name in subscriptions_to_delete:
            itm.delete()
            log.info(f"Endpoint deleted {endpoint}")


def sns_to_sqs_policy(topic_arn, queue_arn):
    policy_document = \
        {
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": [
                    "SQS:SendMessage"
                ],
                "Resource": queue_arn,
                "Condition": {
                    "ArnEquals": {
                        "aws:SourceArn": topic_arn
                    }
                }
            }]
        }
    return policy_document


def allow_sns_to_write_to_sqs(topic_arn, queue_arn, queue_url):
    client = boto3.client('sqs')
    policy_json = sns_to_sqs_policy(topic_arn, queue_arn)

    response = client.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={
            'Policy': json.dumps(policy_json)
        }
    )
    log.debug(response)


def set_dead_letter_queue(queue_name, topic_name):
    client = boto3.client('sns')
    queue_data = sqs_manager.get_queue_by_name(queue_name)

    if not queue_data:
        log.error(f"Not queue found under name {queue_name}")
        return

    dead_letter_queue_arn = queue_data.attributes["QueueArn"]
    response = create_subscription(topic_name, "sqs", dead_letter_queue_arn)

    if not response:
        return

    redrive_policy = {'deadLetterTargetArn': dead_letter_queue_arn}

    # Configure queue to send messages to dead letter queue
    client.set_subscription_attributes(
        SubscriptionArn=response,
        AttributeName='RedrivePolicy',
        AttributeValue=json.dumps(redrive_policy)
    )

    q_url = sqs_manager.get_queue_urls(queue_name)
    topic_arn = get_topic_by_name(topic_name)[0]["TopicArn"]

    # allow queue to receive msg from sns
    allow_sns_to_write_to_sqs(topic_arn=topic_arn,
                              queue_arn=dead_letter_queue_arn,
                              queue_url=q_url)

##############################################################################################
