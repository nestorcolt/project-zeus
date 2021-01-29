from Cloud.packages.dynamo import controller, dynamo_manager
from Cloud.packages.constants import constants
from Cloud.packages.sns import sns_manager
from collections import OrderedDict
import threading
import timeit
import boto3
import time


##############################################################################################

def create_or_update_log(log_group, log_stream, message):
    """
    message will be a python dictionary
    """
    client = boto3.client('logs')

    try:
        client.create_log_group(logGroupName=log_group)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    try:
        client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    response = client.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=log_stream)

    event_log = {
        'logGroupName': log_group,
        'logStreamName': log_stream,
        'logEvents': [
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': message
            }
        ],
    }

    if 'uploadSequenceToken' in response['logStreams'][0]:
        event_log.update({'sequenceToken': response['logStreams'][0]['uploadSequenceToken']})

    response = client.put_log_events(**event_log)
    return response


##############################################################################################
# STATS

def create_thread_process(function=None, arguments=()):
    """
    A helper function to run process on different threads in the CPU to avoid the machine being freeze during a main
    thread logic execution
    :param function: (func) function to call inside of fetched module
    :param arguments: list of arguments that will be set into the function call
    :return:
    """
    # Make the thread
    thread_process = threading.Thread(target=function, args=arguments)
    # Start the thread
    thread_process.start()


def get_user_stats(user_id):
    user_data = dynamo_manager.read_item(constants.USERS_TABLE_NAME, constants.TABLE_PK, user_id)
    offer_list = controller.get_offers(user_id)

    validated_count = len([itm for itm in offer_list if itm["validated"] is True])
    user_block_count = len(controller.get_blocks(user_id))
    user_offer_count = len(offer_list)

    search_state = user_data["search_blocks"]
    last_active = user_data["last_active"]

    # the user state on the search engine
    sleep_time = controller.get_past_time_span(constants.SEARCH_SLEEP_TIME_THRESHOLD)
    user_state = "Active"

    if search_state and last_active > sleep_time:
        user_state = "Stopped"
    if last_active < sleep_time:
        user_state = "Paused"
    if not search_state:
        user_state = "Inactive"

    output = OrderedDict({})
    output["search_status"] = user_state
    output["total_offers"] = user_offer_count
    output["validated_offers"] = validated_count
    output["accepted_offers"] = user_block_count

    return output


def stats_to_string(stats_dict):
    result = ""

    for key, value in stats_dict.items():
        title = key.title().replace("_", " ")
        joined = f"{title}: {value} | "
        result += joined

    return result[:-2]


def log_user_stats(user_id):
    stats = get_user_stats(user_id)
    stats_message = stats_to_string(stats)
    topic_arn = sns_manager.get_topic_by_name(constants.SE_LOGS_TOPIC)[0]["TopicArn"]
    sns_manager.sns_publish_to_topic(topic_arn, stats_message, constants.USER_PLACEHOLDER.format(user_id))


def log_all_users():
    last_active = controller.get_last_active_users()

    for user_data in last_active["Items"]:
        search_blocks = user_data.get("search_blocks")

        if search_blocks:
            user = user_data[constants.TABLE_PK]
            thread_process = threading.Thread(target=log_user_stats, args=[user])
            thread_process.start()

##############################################################################################
