from Cloud.packages.dynamo import dynamo_manager
from Cloud.packages.constants import constants
import requests
import time
import json

##############################################################################################
# END POINT TO REGISTER THE BLOCK CHECK IN
URL = "https://rabbit.amazon.com/RefreshItinerary"


##############################################################################################

def get_check_in_data(refresh_token, longitude, latitude):
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
                "time": time.time()
            }
        }
    })

    return check_in_data


##############################################################################################

def get_user_data(user_request):
    user_id = user_request.get("user_id")

    if user_id is None:
        return

    user_data = dynamo_manager.read_item(constants.USERS_TABLE_NAME, constants.TABLE_PK, user_id)

    if user_data is None:
        print(f"Not user found with ID: {user_id}")
        return

    return user_data


def check_in_block(block_data):
    user_data = get_user_data(block_data)

    if user_data is None:
        return

        # create the body to send as json in the POST request
    check_in_data = get_check_in_data(user_data.get("refresh_token", ""),
                                      block_data.get("longitude"),
                                      block_data.get("latitude"))

    # Create post request
    authorization_header = {"x-amz-access-token": user_data.get("access_token", "")}
    response = requests.post(URL, json=check_in_data, headers=authorization_header, timeout=5)

    if response.status_code == 200:
        message = "Block checked in successfully!"
    elif response.status_code == 410:
        message = "Forbidden or bad request"
    else:
        message = "Something happened in the request. Operation failed."

    # Continue logic to handle more cases
    print(message, response)
    return {"response": response, "message": message}


##############################################################################################
check_in_block({"user_id": "5", "longitude": "", "latitude": ""})
