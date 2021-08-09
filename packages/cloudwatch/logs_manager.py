from Cloud.packages.dynamo import controller, dynamo_manager
from Cloud.packages.constants import constants
from Cloud.packages.sns import sns_manager
from Cloud.packages.utilities import utils
from collections import OrderedDict
from pprint import pprint
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


def get_user_stats(user_id):
    user_data = dynamo_manager.read_item(constants.USERS_TABLE_NAME, constants.TABLE_PK, user_id)

    # No user found
    if user_data is None:
        return

    stats = controller.get_user_stats(user_id)

    if stats is None:
        return

    user_offer_count = stats[0]
    user_block_count = stats[1]
    validated_count = stats[2]

    search_state = user_data.get("search_blocks", False)
    last_active = user_data.get("last_active", 0)
    asleep_time = utils.get_time_difference(last_active, utils.get_unix_time())

    # the user state on the search engine
    user_state = "Active"

    if last_active != 0 and asleep_time < constants.SEARCH_SLEEP_TIME_THRESHOLD:
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

    if stats:
        stats_message = stats_to_string(stats)
        topic_arn = sns_manager.get_topic_by_name(constants.SE_LOGS_TOPIC)[0]["TopicArn"]
        sns_manager.sns_publish_to_topic(topic_arn, stats_message, constants.USER_PLACEHOLDER.format(user_id))


def describe_search_engine_logs(user_id=None):
    """
    Describe all the logs from the search engine in the last 24 hours
    """
    client = boto3.client('logs')
    minutes_in_day = 1440

    # this will be returned with "key:user log name, value: list of logged messages in the last 24 hours"
    output_data_dict = {}

    log_stream_name = "User-{}".format(user_id)

    response = client.get_log_events(
        logGroupName=constants.SEARCH_ENGINE_LOG_GROUP,
        logStreamName=log_stream_name,
        endTime=int(utils.get_unix_time()) * 1000,
        startTime=int(utils.get_past_time_span(minutes_in_day)) * 1000,
    )

    events = response["events"]

    output_data_dict["log_data"] = {"user_id": user_id, "events": events}

    return output_data_dict

##############################################################################################
