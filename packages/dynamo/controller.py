from Cloud.packages.dynamo import dynamo_manager
from Cloud.packages.constants import constants
from boto3.dynamodb.conditions import Key, Attr
from Cloud.packages.utilities import utils
from Cloud.packages import logger
from decimal import Decimal

LOGGER = logger.Logger(__name__)
log = LOGGER.logger

cst = constants


##############################################################################################
# Users Table

def get_last_active_users():
    table = dynamo_manager.get_table_by_name(constants.USERS_TABLE_NAME)
    wait_time_span = utils.get_past_time_span(constants.SEARCH_SLEEP_TIME_THRESHOLD)
    response = table.scan(FilterExpression=Attr(constants.USER_LAST_ACTIVE_PROPERTY).lt(Decimal(wait_time_span)))
    return response


def get_all_users():
    table = dynamo_manager.get_table_by_name(constants.USERS_TABLE_NAME)
    response = table.scan()
    return response


def set_last_active_user_time(user_id):
    unix_seconds = utils.get_unix_time()

    item = {constants.USER_LAST_ACTIVE_PROPERTY: Decimal(unix_seconds)}

    dynamo_manager.update_item(constants.USERS_TABLE_NAME,
                               constants.TABLE_PK,
                               user_id,
                               item)


##############################################################################################
# Blocks Table

def get_blocks(user_id=None):
    table = dynamo_manager.get_table_by_name(constants.BLOCKS_TABLE_NAME)

    if user_id is None:
        response = table.scan()
    else:
        response = table.query(KeyConditionExpression=Key(constants.TABLE_PK).eq(user_id))

    items = response.get("Items")

    if items:
        return items

    return []


def put_new_block(user_id, block_data):
    captured_time = utils.get_unix_time()
    hours_to_minutes = constants.CLEANUP_OFFERS_TIME_THRESHOLD * 60
    expiration_date = utils.get_future_time_span(hours_to_minutes)

    try:
        block_start_time = block_data["startTime"]
        block_area_id = block_data["serviceAreaId"]
    except Exception as e:
        log.error(f"Error: {e} not found in block data")
        return e

    new_item = {constants.TABLE_PK: user_id,
                constants.BLOCK_SORT_KEY: Decimal(captured_time),
                constants.BLOCK_STATION_KEY: block_area_id,
                constants.BLOCK_TIME_KEY: Decimal(block_start_time),
                constants.TTL_ATTR_KEY: Decimal(expiration_date),
                constants.BLOCK_DATA_KEY: block_data}

    # creates the new entry on dynamo block table
    dynamo_manager.create_item(constants.BLOCKS_TABLE_NAME, utils.map_request_body({}, new_item))


##############################################################################################
# Offers to create analytics

def put_new_offer(user_id, validated, offer_data):
    captured_time = utils.get_unix_time()
    hours_to_minutes = constants.CLEANUP_OFFERS_TIME_THRESHOLD * 60
    expiration_date = utils.get_future_time_span(hours_to_minutes)

    try:
        offer_id = offer_data["offerId"]
        offer_area_id = offer_data["serviceAreaId"]
    except Exception as e:
        log.error(f"Error: {e} not found in block data")
        return e

    new_item = {constants.TABLE_PK: user_id,
                constants.OFFER_SORT_KEY: offer_id,
                constants.OFFER_VALIDATED_KEY: validated,
                constants.OFFER_STATION_ID: offer_area_id,
                constants.OFFER_TIME_KEY: Decimal(captured_time),
                constants.TTL_ATTR_KEY: Decimal(expiration_date),
                constants.OFFER_DATA_KEY: offer_data}

    # creates the new entry on dynamo block table
    dynamo_manager.create_item(constants.OFFERS_TABLE_NAME, utils.map_request_body({}, new_item))


def get_offers(user_id=None):
    table = dynamo_manager.get_table_by_name(constants.OFFERS_TABLE_NAME)

    if user_id is None:
        return ["Need to specify an user to query"]
    else:
        response = table.query(KeyConditionExpression=Key(constants.TABLE_PK).eq(user_id))

    return response["Items"]


def offer_exists(user_id=None, offer_id=None):
    table = dynamo_manager.get_table_by_name(constants.OFFERS_TABLE_NAME)

    if user_id is None and offer_id is None:
        return ["Need to specify an user to query"]
    else:
        response = table.query(
            KeyConditionExpression=Key(constants.TABLE_PK).eq(user_id) & Key(constants.OFFER_SORT_KEY).eq(offer_id)
        )

    if response["Items"]:
        return True

    return False


##############################################################################################
# Statistics Table

def create_user_stats(user_id=None):
    """
    Create the entry with the stats at zero value
    """
    item = {cst.STS_OFFER_KEY: 0,
            cst.STS_ACCEPTED_KEY: 0,
            cst.STS_VALIDATED_KEY: 0}

    # Create the item if doesnt exist yet
    dynamo_manager.update_item(table_name=constants.STATISTICS_TABLE_NAME,
                               primary_key=constants.TABLE_PK,
                               value=user_id,
                               items=item)


def update_user_stats(user_id=None, offer=0, validated=0, accepted=0):
    """
    Works with Atomic counter feature from dynamo db to increment the counter properties from this table
    """
    table = dynamo_manager.get_table_by_name(constants.STATISTICS_TABLE_NAME)

    # Check for item exists first
    response = table.query(KeyConditionExpression=Key(constants.TABLE_PK).eq(user_id))

    if not response["Items"]:
        create_user_stats(user_id)

    # Increment the atomic counters
    exp = "set offers = offers + :offer, validated = validated + :valid, accepted = accepted + :accept"
    table.update_item(Key={constants.TABLE_PK: user_id},
                      UpdateExpression=exp,
                      ExpressionAttributeValues={
                          ':offer': offer,
                          ':valid': validated,
                          ':accept': accepted})


def reset_user_stats(user_id):
    """
    Set back to zero the stats for this user
    """
    create_user_stats(user_id)


def get_user_stats(user_id):
    table = dynamo_manager.get_table_by_name(constants.STATISTICS_TABLE_NAME)

    try:
        response = table.query(KeyConditionExpression=Key(constants.TABLE_PK).eq(user_id))
        user_data = response["Items"]

        if user_data:
            user_data = user_data[0]
            return [user_data[cst.STS_OFFER_KEY], user_data[cst.STS_ACCEPTED_KEY], user_data[cst.STS_VALIDATED_KEY]]

    except Exception as e:
        log.error(e)
        return False

##############################################################################################
