from Cloud.packages.dynamo import dynamo_manager
from Cloud.packages.constants import constants
from pprint import pprint
from uuid import uuid4
import requests
import time
import json

##############################################################################################
ACCESS_HEADERS = {"app_name": "com.amazon.rabbit",
                  "source_token_type": "refresh_token",
                  "source_token": "refresh_token",
                  "requested_token_type": "access_token"}

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
    headers = ACCESS_HEADERS.copy()
    headers["source_token"] = refresh_token
    response = requests.post(constants.AMAZON_API_AUTHENTICATION_URL, data=headers)
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
        return

    post_data = {"TransportationMode": "DRIVING",
                 "serviceAreaId": service_area_id}

    response = requests.post(url=constants.AUTH_SESSIONS_URL,
                             json=post_data,
                             headers=get_authorization_header(access_token),
                             timeout=5)

    pprint(response.json())


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
