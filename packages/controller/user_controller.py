from packages.dynamo import dynamo_manager
from packages.constants import constants
import requests

##############################################################################################
# GLOBALS
ACCESS_HEADERS = {"app_name": "com.amazon.rabbit",
                  "source_token_type": "refresh_token",
                  "source_token": "refresh_token",
                  "requested_token_type": "access_token"}


##############################################################################################
# Controller functions:

def get_authorization_header(access_token):
    authorization_header = {"x-amz-access-token": access_token}
    return authorization_header


def get_user_data(user_request):
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


def get_schedule(access_token, refresh_token):
    response = requests.get(url=constants.SCHEDULE_URL, headers=get_authorization_header(access_token), timeout=5)

    if response.status_code in [401, 403]:
        new_a_token = get_access_token(refresh_token)

        if new_a_token is not None:
            response = requests.get(url=constants.SCHEDULE_URL,
                                    headers=get_authorization_header(new_a_token),
                                    timeout=5)

    response_json = response.json()
    schedule = response_json.get("scheduledAssignments", None)
    return schedule


##############################################################################################
if __name__ == '__main__':
    user_data = get_user_data({"user_id": "5"})
    get_schedule(user_data["access_token"], user_data["refresh_token"])
