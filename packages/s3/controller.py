from Cloud.packages.constants import constants
from Cloud.packages.utilities import utils
from Cloud.packages import logger
import boto3
import json

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################
# default functions

def put_object(bucket_name, bucket_key, content):
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, bucket_key).put(Body=content)


def read_object(bucket_name, bucket_key):
    s3 = boto3.resource('s3')

    try:
        string_content = s3.Object(bucket_name, bucket_key).get()['Body'].read().decode('utf-8')
    except Exception as e:
        print(e)
        return None

    return string_content


def delete_object_from_bucket(bucket_name, bucket_key):
    s3 = boto3.resource('s3')

    try:
        s3.Object(bucket_name, bucket_key).delete()
    except:
        pass


##############################################################################################
# offers handlers

def put_new_offer(offer_dictionary, user_id, validated, offer_data):
    user_dict = offer_dictionary.get(user_id, {})
    captured_time = utils.get_unix_time()

    try:
        offer_id = offer_data["offerId"]
        offer_area_id = offer_data["serviceAreaId"]
    except Exception as e:
        log.error(f"Error: {e} not found in block data")
        return e

    new_item = {
        constants.OFFER_VALIDATED_KEY: validated,
        constants.OFFER_STATION_ID: offer_area_id,
        constants.OFFER_TIME_KEY: captured_time,
        constants.OFFER_DATA_KEY: offer_data
    }

    user_dict[offer_id] = new_item
    offer_dictionary[user_id] = user_dict

    return offer_dictionary


def read_users_offers_stats():
    offer_dictionary = read_object(constants.OFFERS_BUCKET_NAME, constants.OFFERS_BUCKET_KEY) or "{}"
    offer_dictionary = json.loads(offer_dictionary)

    if offer_dictionary == {}:
        return {}

        # this dict will contain all the absolute values to dump in the table
    handler_dict = {}

    for user, offers in offer_dictionary.items():
        validated_count = 0
        for offer in offers.values():
            validated = offer["validated"]
            validated_count += int(validated)

        # update dict with absolute data
        handler_dict[user] = {"offers": len(offers), "valid": validated_count}

    return handler_dict

##############################################################################################
