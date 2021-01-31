from Cloud.packages.security import secrets_manager
from Cloud.packages.constants import constants
from Cloud.packages.utilities import utils
from Cloud.packages import logger
from decimal import Decimal
import requests

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################
def web_app_auth():
    secrets = secrets_manager.get_secret(constants.WEB_AUTH_SECRETS)
    response = requests.post(constants.WEB_BACKEND_AUTHENTICATION_URL, body=secrets)

    if response.status_code == 200:
        data = response.json()
        return data["data"][constants.WEB_API_TOKEN_KEY]
    else:
        return False


def send_block_to_web(user_id, block_data, **kwargs):
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
    response = requests.post(constants.WEB_BACKEND_ENDPOINT_URL,
                             body=new_item,
                             headers=kwargs["access_token"])
    return response


def send_error_to_web(user_id, **kwargs):
    response = requests.post(constants.WEB_BACKEND_ERROR_ENDPOINT_URL,
                             body=user_id,
                             headers=kwargs["access_token"])
    return response

##############################################################################################
