from Cloud.packages.constants import constants
from Cloud.packages.utilities import utils
from Cloud.packages import logger
from decimal import Decimal
import requests

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################

def send_block_to_web(user_id, block_data):
    captured_time = utils.get_unix_time()

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
    response = requests.post(constants.WEB_BACKEND_ENDPOINT_URL, data=new_item)
    return response


def send_error_to_web(user_id):
    response = requests.post(constants.WEB_BACKEND_ERROR_ENDPOINT_URL, data={"user_id": user_id})
    return response
