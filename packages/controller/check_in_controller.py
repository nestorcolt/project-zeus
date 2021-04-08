from packages.controller.user_controller import get_authorization_header, get_user_data, get_access_token
from Cloud.packages.constants import constants
from pprint import pprint
import requests
import time
import json


##############################################################################################

def get_check_in_data(refresh_token, longitude, latitude):
    """
    Makes the header with the check in data and return this to parse the the api call
    """
    check_in_data = json.dumps({
        "refreshToken": refresh_token,
        "startTransporterSession": False,
        "transporterContext": {
            "marketplaceId": "ATVPDKIKX0DER",
            "transporterLocation": {
                "marketplaceId": "ATVPDKIKX0DER",
                "accuracy": 6.067999839782715,
                "altitude": -22.0,
                "latitude": latitude,
                "longitude": longitude,
                "provider": "gps",
                "time": int(time.time())
            }
        }
    })

    return check_in_data


##############################################################################################


def check_in_block(block_data):
    """
    The check in block logic to pass to call inside lambda function
    """
    user_data = get_user_data(block_data)

    if user_data is None:
        return

    refresh_token = user_data.get("refresh_token", None)

    if refresh_token is None:
        return

    # create the body to send as json in the POST request
    check_in_data = get_check_in_data(refresh_token,
                                      block_data.get("longitude"),
                                      block_data.get("latitude"))

    # Create post request
    authorization_header = get_authorization_header(get_access_token(refresh_token))
    response = requests.post(constants.CHECK_IN_URL,
                             json=json.dumps(check_in_data),
                             headers=authorization_header,
                             timeout=5)

    pprint(response.content)

    if response.status_code == 200:
        message = "Block checked in successfully!"
    elif response.status_code == 410:
        message = "Forbidden or bad request"
    else:
        message = "Something happened in the request. Operation failed."

    print(message, response)
    return {"response": response, "message": message}


##############################################################################################
user_id = "5"
# user_data = get_user_data({"user_id": user_id})
# get_schedule(user_data["access_token"], user_data["refresh_token"])
# check_in_block({"user_id": user_id, "longitude": "-80.323221", "latitude": "25.67329"})
