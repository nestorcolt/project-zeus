from Cloud.packages.dynamo import dynamo_manager
from Cloud.packages.constants import constants
from pprint import pprint
from uuid import uuid4
import requests
import time
import json

##############################################################################################

"""

Side note: the API_DEFAULT_HEADERS are used in amazon request to their api's, however I've tested this and they are not
necessary to make them work. I will keep them here in case in some future I know where they are.

"""

API_DEFAULT_HEADERS = {
    "x-flex-instance-id": str(uuid4()),
    "X-Flex-Client-Time": str(int(time.time())),
    "Content-Type": "application/json",
    "User-Agent": f'Dalvik/2.1.0 (Linux; U; Android 7.1.2; {constants.DEVICE_MODEL} Build/N2G48C) RabbitAndroid/{constants.APP_VERSION}',
    "X-Amzn-RequestId": str(uuid4()),
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}


##############################################################################################
# Controller functions:

def get_authorization_header(access_token, default_headers=None):
    """
    Gets a new authorization dictionary ready with the headers to send to amazon request.
    Will accept an extra dictionary with other headers that amazon uses, although they are not necessary
    to make request to the api. This has been proved
    """
    authorization_header = {"x-amz-access-token": access_token}

    if default_headers:
        authorization_header.update(default_headers)

    return authorization_header


def get_user_data(user_request):
    """
    Read the users table in dynamo DB and fetch the data of the given user in the request
    """
    user_id = user_request.get("user_id")

    if user_id is None:
        return

    user_data = dynamo_manager.read_item(constants.USERS_TABLE_NAME, constants.TABLE_PK, user_id)

    if user_data is None:
        print(f"Not user found with ID: {user_id}")
        return

    return user_data


def get_access_token(refresh_token):
    """
    Makes a request to the authentication api of amazon and get a new access token
    refresh_token: string - the refresh token of the user necessary to request an access token
    """
    access_headers = {"app_name": "com.amazon.rabbit", "source_token_type": "refresh_token",
                      "source_token": refresh_token, "requested_token_type": "access_token"}

    response = requests.post(constants.AMAZON_API_AUTHENTICATION_URL, data=access_headers)
    json_response = response.json()
    return json_response.get("access_token", None)


def get_service_area_id(access_token):
    """
    Get the flex client service area id code
    """
    response = requests.get(url=constants.SERVICE_AREA_URL, headers=get_authorization_header(access_token), timeout=5)
    json_obj = response.json()
    _id = json_obj.get("serviceAreaIds", [])

    if _id:
        return _id[0]


def authenticate_user_session(access_token, service_area_id):
    """
    Authenticate the session of the flex user as it was doing it with the app taking a picture to validate
    is the same owner of the account
    """
    if not service_area_id or not access_token:
        return 404

    post_data = {"TransportationMode": "DRIVING",
                 "serviceAreaId": service_area_id}

    response = requests.post(url=constants.AUTH_SESSIONS_URL,
                             json=post_data,
                             headers=get_authorization_header(access_token),
                             timeout=5)

    return response.status_code


def get_schedule(access_token, refresh_token):
    """
    Get the schedule (blocks) that a user has on the calendar to deliver
    """
    response = requests.get(url=constants.SCHEDULE_URL, headers=get_authorization_header(access_token), timeout=5)

    if response.status_code in [401, 403]:
        new_a_token = get_access_token(refresh_token)

        if new_a_token is not None:
            response = requests.get(url=constants.SCHEDULE_URL,
                                    headers=get_authorization_header(new_a_token),
                                    timeout=5)

    response_json = response.json()
    schedule = response_json.get("scheduledAssignments", None)
    pprint(schedule)
    return schedule

##############################################################################################
