from modules import logger
import boto3

LOGGER = logger.Logger("SQS")
LOGGER.set_file_handle()
log = LOGGER.logger


##############################################################################################

def get_queue_by_name(name):
    client = boto3.client('sqs')
    queues = client.list_queues(QueueNamePrefix=name)
    urls = queues.get("QueueUrls", None)
    return urls


def create_queue(name):
    client = boto3.client('sqs')

    try:
        response = client.create_queue(QueueName=name)
        log.debug(response)

    except Exception as e:
        log.exception(e)


def remove_queue(name):
    client = boto3.client('sqs')
    queue_url = get_queue_by_name(name)

    if not queue_url:
        return

    try:
        response = client.delete_queue(QueueUrl=queue_url[0])
        log.debug(response)

    except Exception as e:
        log.exception(e)

##############################################################################################
