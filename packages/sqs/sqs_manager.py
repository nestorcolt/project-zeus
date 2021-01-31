from Cloud.packages.constants import constants
from Cloud.packages import logger
import boto3
import json

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################

def get_queue_by_name(name):
    """
    Return the queue object
    :param name:
    :return:
    """
    client = boto3.client('sqs')
    queues = client.list_queues().get("QueueUrls", None)

    if queues is None:
        return

    for q_url in queues:
        if q_url.endswith(name):
            sqs = boto3.resource('sqs')
            queue = sqs.Queue(q_url)
            return queue


def get_queue_urls(name):
    result = get_queue_by_name(name)

    if not result:
        return

    return result.url


def create_queue(name):
    client = boto3.client('sqs')

    try:
        response = client.create_queue(QueueName=name)
        log.debug(response)

    except Exception as e:
        log.exception(e)


def remove_queue(name):
    client = boto3.client('sqs')
    queue_url = get_queue_urls(name)

    if not queue_url:
        return

    try:
        response = client.delete_queue(QueueUrl=queue_url)
        log.debug(response)

    except Exception as e:
        log.exception(e)


def send_message_to_queue(queue_name, message):
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    # Create a new message
    queue.send_message(MessageBody=message)


def get_messages_from_queue(queue_name):
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    response = boto3.client("sqs").receive_message(QueueUrl=queue.url)
    messages = response.get("Messages")

    if messages:
        return response["Messages"]

    return []


def get_user_in_queue_body(user_id, queue_name):
    messages = get_messages_from_queue(queue_name)
    result = list(map(lambda itm: json.loads(itm["Body"]).get(constants.TABLE_PK) == user_id, messages))

    if result:
        return result[0]

    return False

##############################################################################################
