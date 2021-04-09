from Cloud.packages.controller import user_controller
from Cloud.packages.constants import constants
from pprint import pprint
import requests
import time
import json


##############################################################################################

def get_check_in_data(longitude, latitude):
    """
    Makes the header with the check in data and return this to parse the the api call
    """
    check_in_data = json.dumps({
        "refreshToken": "placeholder",
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
                "time": str(int(time.time()))
            }
        }
    })

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
    authorization_header = user_controller.get_authorization_header(user_controller.get_access_token(refresh_token))
    response = requests.post(constants.CHECK_IN_URL,
                             data=check_in_data,
                             headers=authorization_header,
                             timeout=5)

    pprint(response.json())

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
    user_id = "31"
    user_data = user_controller.get_user_data({"user_id": user_id})
    user_controller.get_schedule(user_data["access_token"], user_data["refresh_token"])
    # check_in_block({"user_id": user_id, "longitude": "-80.323221", "latitude": "25.67329"})
