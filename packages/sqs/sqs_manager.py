from packages import logger
import boto3

LOGGER = logger.Logger("SQS")
LOGGER.set_file_handle()
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

##############################################################################################
