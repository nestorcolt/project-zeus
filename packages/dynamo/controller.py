from Cloud.packages.dynamo import dynamo_manager
from Cloud.packages.constants import constants
from boto3.dynamodb.conditions import Key, Attr
from Cloud.packages import logger
from decimal import Decimal
from time import mktime
import collections.abc
import datetime
import pprint

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################
# Some utilities for table operations

def get_unix_time():
    t = datetime.datetime.now()
    unix_secs = mktime(t.timetuple())
    return unix_secs


def get_future_time_span(minutes):
    unix_timestamp_future = get_unix_time() + (minutes * 60)  # N min * 60 seconds
    return unix_timestamp_future


def get_past_time_span(minutes):
    unix_timestamp_future = get_unix_time() - (minutes * 60)  # N min * 60 seconds
    return unix_timestamp_future


def to_decimal(value):
    if isinstance(value, float):
        return Decimal(value)

    return value


def map_request_body(new_dict, old_dict):
    for key, value in old_dict.items():
        if isinstance(value, collections.abc.Mapping):
            new_dict[key] = map_request_body(new_dict.get(key, {}), to_decimal(value))
        else:
            new_dict[key] = to_decimal(value)

    return new_dict


##############################################################################################
# Users Table

def get_last_active_users():
    table = dynamo_manager.get_table_by_name(constants.USERS_TABLE_NAME)
    wait_time_span = get_past_time_span(constants.EC2_SLEEP_TIME_THRESHOLD)
    response = table.scan(FilterExpression=Attr(constants.USER_LAST_ACTIVE_PROPERTY).lt(Decimal(wait_time_span)))
    return response


##############################################################################################
# Blocks Table

def get_user_blocks(user_id):
    table = dynamo_manager.get_table_by_name(constants.BLOCKS_TABLE_NAME)
    response = table.scan(FilterExpression=Key(constants.TABLE_PK).eq(user_id))
    items = response.get("Items")
    pprint.pprint(items)

    if items:
        return items


def put_new_block(user_id, block_data):
    captured_time = get_unix_time()

    try:
        block_start_time = block_data["startTime"]
        block_area_id = block_data["serviceAreaId"]
    except Exception as e:
        log.error(f"Error: {e} not found in block data")
        return e

    new_item = {constants.TABLE_PK: user_id,
                constants.BLOCK_SORT_KEY: Decimal(block_start_time),
                constants.BLOCK_STATION_KEY: block_area_id,
                constants.BLOCK_TIME_KEY: Decimal(captured_time),
                constants.BLOCK_DATA_KEY: block_data}

    # creates the new entry on dynamo block table
    dynamo_manager.create_item(constants.BLOCKS_TABLE_NAME, map_request_body({}, new_item))


def delete_block(user_id, block_id):
    # creates the new entry on dynamo block table
    table = dynamo_manager.get_table_by_name(constants.BLOCKS_TABLE_NAME)

    try:
        table.delete_item(
            Key={
                constants.TABLE_PK: user_id,
                constants.BLOCK_SORT_KEY: block_id,
            },
        )
    except Exception as e:
        dynamo_manager.log.error(e)


def cleanup_blocks_table():
    """
    Clean up the table blocks from blocks older than 48 hours from the time the function is called
    """
    table = dynamo_manager.get_table_by_name(constants.BLOCKS_TABLE_NAME)
    hours_to_minutes = constants.CLEANUP_BLOCKS_TIME_THRESHOLD * 60
    wait_time_span = get_past_time_span(hours_to_minutes)
    response = table.scan(FilterExpression=Attr(constants.BLOCK_SORT_KEY).lt(Decimal(wait_time_span)))

    for item in response["Items"]:
        user_id = item[constants.TABLE_PK]
        block_id = item[constants.BLOCK_SORT_KEY]
        delete_block(user_id, block_id)

##############################################################################################
