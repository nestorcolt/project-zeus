from Cloud.packages.security import secrets_manager
from Cloud.packages.constants import constants
from Cloud.packages.utilities import utils
from Cloud.packages import logger
import requests
import json

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################


def web_app_auth():
    secrets = secrets_manager.get_secret(constants.WEB_AUTH_SECRETS)

    try:
        response = requests.post(constants.WEB_BACKEND_AUTHENTICATION_URL, json=json.loads(secrets))

        if response.status_code == 200:
            data = response.json()
            token = data["data"]["jwToken"].strip('"')
            secrets_manager.update_secret(constants.WEB_AUTH_TOKEN_SECRET, token)
            return token

    except Exception as e:
        log.debug(e)
        return None


def authorize_request(function):
    """
    Authorizes the request to the web app
    """

    def func_wrapper(*args, **kwargs):
        token = secrets_manager.get_secret(constants.WEB_AUTH_TOKEN_SECRET)
        kwargs["access_token"] = {"Authorization": "Bearer " + token.strip('"')}
        status_code = function(*args, **kwargs)

        if status_code != 200:
            response = web_app_auth()

            if response:
                kwargs["access_token"] = {"Authorization": "Bearer " + response.strip('"')}
                status_code = function(*args, **kwargs)

        return status_code

    return func_wrapper


@authorize_request
def send_block_to_web(user_id, block_data, **kwargs):
    captured_time = utils.get_unix_time()

    try:
        block_start_time = block_data["startTime"]
        block_area_id = block_data["serviceAreaId"]
    except Exception as e:
        log.error(f"Error: {e} not found in block data")
        return e

    new_item = {constants.TABLE_PK: user_id,
                constants.BLOCK_SORT_KEY: captured_time,
                constants.BLOCK_STATION_KEY: block_area_id,
                constants.BLOCK_TIME_KEY: block_start_time,
                constants.BLOCK_DATA_KEY: block_data}

    # creates the new entry on dynamo block table
    response = requests.post(constants.WEB_BACKEND_ENDPOINT_URL,
                             json=new_item,
                             headers=kwargs["access_token"])

    return response.status_code


@authorize_request
def send_error_to_web(user_id, **kwargs):

    print(constants.WEB_BACKEND_ERROR_ENDPOINT_URL)
    print(json.dumps({"user_id": user_id}))
    headers = kwargs["access_token"]
    print(headers)

    response = requests.post(constants.WEB_BACKEND_ERROR_ENDPOINT_URL,
                             json=json.dumps({"user_id": user_id}),
                             headers=kwargs["access_token"])

    return response.status_code

##############################################################################################
