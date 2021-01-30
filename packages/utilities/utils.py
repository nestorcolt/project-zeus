from Cloud.packages import logger
from decimal import Decimal
from time import mktime
import collections.abc
import datetime

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################
# Some utilities
def get_unix_time():
    t = datetime.datetime.now()
    unix_secs = mktime(t.timetuple())
    return unix_secs


def convert_unix_time_to_human(seconds):
    return datetime.datetime.fromtimestamp(int(seconds)).strftime('%H:%M:%S')


def get_time_difference(first, second):
    result = abs(int(first) - int(second)) / 60
    return result


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


def to_float(value):
    if isinstance(value, Decimal):
        return float(value)

    return value


def map_request_body(new_dict, old_dict):
    for key, value in old_dict.items():
        if isinstance(value, collections.abc.Mapping):
            new_dict[key] = map_request_body(new_dict.get(key, {}), to_decimal(value))
        else:
            new_dict[key] = to_decimal(value)

    return new_dict


def map_response_body(new_dict, old_dict):
    for key, value in old_dict.items():
        if isinstance(value, collections.abc.Mapping):
            new_dict[key] = map_response_body(new_dict.get(key, {}), to_float(value))
        else:
            new_dict[key] = to_float(value)

    return new_dict

##############################################################################################
