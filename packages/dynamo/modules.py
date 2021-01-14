from Cloud.packages.dynamo import dynamo_manager
from Cloud.packages.constants import constants
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from time import mktime
import datetime


##############################################################################################
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


def get_last_active_users():
    table = dynamo_manager.get_table_by_name(constants.USERS_TABLE_NAME)
    wait_time_span = get_past_time_span(constants.EC2_SLEEP_TIME_THRESHOLD)
    response = table.scan(FilterExpression=Attr(constants.USER_LAST_ACTIVE_PROPERTY).lt(Decimal(wait_time_span)))
    return response

##############################################################################################
