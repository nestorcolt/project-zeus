from sqs import sqs_manager
from modules import logger
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


def sns_to_sqs_policy(topic_arn, queue_arn):
    policy_document = """{{
      "Statement":[
        {{
          "Sid":"MyPolicy",
          "Effect":"Allow",
          "Principal" : {{"AWS" : "*"}},
          "Action":"SQS:SendMessage",
          "Resource": "{}",
          "Condition":{{
            "ArnEquals":{{
              "aws:SourceArn": "{}"
            }}
          }}
        }}
      ]
    }}""".format(queue_arn, topic_arn)

    return policy_document


def allow_sns_to_write_to_sqs(topic_arn, queue_arn, queue_url):
    client = boto3.client('sqs')
    policy_json = sns_to_sqs_policy(topic_arn, queue_arn)

    response = client.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={
            'Policy': policy_json
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

    # allow queue to receive msg from sns
    allow_sns_to_write_to_sqs(topic_arn=response,
                              queue_arn=dead_letter_queue_arn,
                              queue_url=q_url)


##############################################################################################

set_dead_letter_queue("SE-DEAD-LETTER-QUEUE", "SE-START-SERVICE")
