from Cloud.packages.controller import user_controller
from Cloud.packages.constants import constants
from pprint import pprint
import importlib
import requests
import time
import json

importlib.reload(user_controller)


##############################################################################################


def get_check_in_data(longitude, latitude):
    """
    Makes the header with the check in data and return this to parse the the api call
    """
    check_in_data = {
        "refreshToken": "placeholder",
        "startTransporterSession": False,
        "transporterContext": {
            "marketplaceId": "ATVPDKIKX0DER",
            "transporterLocation": {
                "accuracy": 6.067999839782715,
                "altitude": -22.0,
                "latitude": latitude,
                "longitude": longitude,
                "provider": "gps",
                "time": int(time.time())
            }
        }
    }

    return check_in_data


##############################################################################################


def check_in_block(block_data):
    """
    The check in block logic to pass to call inside lambda function
    """
    user_data = user_controller.get_user_data(block_data)

    if user_data is None:
        return

    refresh_token = user_data.get("refresh_token", None)

    if refresh_token is None:
        return

    # create the body to send as json in the POST request
    check_in_data = get_check_in_data(block_data.get("longitude"),
                                      block_data.get("latitude"))

    # Create post request
    access_token = user_controller.get_access_token(refresh_token)
    service_area_id = user_controller.get_service_area_id(access_token)
    user_controller.authenticate_user_session(access_token, service_area_id)

    response = requests.post(constants.CHECK_IN_URL,
                             json=check_in_data,
                             headers=user_controller.get_authorization_header(access_token),
                             timeout=7)

    if response.status_code == 200:
        message = "Block checked in successfully!"
    elif response.status_code == 410:
        message = "Forbidden or bad request"
    else:
        message = "Something happened in the request. Operation failed."

    print()
    print(message, response)
    return {"response": response, "message": message}


##############################################################################################
if __name__ == '__main__':
    user_id = "5"
    user_data = user_controller.get_user_data({"user_id": user_id})
    refresh_token = user_data["refresh_token"]
    access_token = user_controller.get_access_token(refresh_token)
    # user_controller.get_schedule(access_token, refresh_token)

    ##############################################################################################

    longitude = -80.251856
    latitude = 26.09688
    # check_in_block({"user_id": user_id, "longitude": longitude, "latitude": latitude})
