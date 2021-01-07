from modules import logger
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
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=name)
    return queue


def get_queue_urls(name):
    client = boto3.client('sqs')
    response = client.get_queue_url(
        QueueName=name,
    )
    return response

print(get_queue_by_name("SE-DEAD-LETTER-QUEUEs"))

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
        response = client.delete_queue(QueueUrl=queue_url["QueueUrls"][0])
        log.debug(response)

    except Exception as e:
        log.exception(e)

##############################################################################################
