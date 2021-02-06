import boto3
import json

USER_POOL_NAME = "bis-api-gateway-cognito-pool"
client = boto3.client('cognito-idp')


##############################################################################################
def authenticate_and_get_token(user_data):
    """

    Authenticate and get the refresh and access token

    """
    body = user_data["body"]

    refresh_token = json.loads(body).get("refreshToken", None)
    username = json.loads(body).get("username")
    password = json.loads(body).get("password")

    response = get_new_access_token(username, refresh_token) if refresh_token is not None else get_bearer_tokens(
        username, password)

    return response


##############################################################################################

def get_cognito_configuration():
    pools = [itm for itm in client.list_user_pools(MaxResults=10)["UserPools"] if itm["Name"] == USER_POOL_NAME]

    if pools:
        client_apps = client.list_user_pool_clients(UserPoolId=pools[0]["Id"])["UserPoolClients"]

        if client_apps:
            return {"pool": pools[0]["Id"], "client": client_apps[0]["ClientId"]}


def get_new_access_token(username, refresh_token):
    config = get_cognito_configuration()

    response = client.initiate_auth(
        ClientId=config["client"],
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            "USERNAME": username,
            'REFRESH_TOKEN': refresh_token,
        }
    )['AuthenticationResult']

    return response


def get_bearer_tokens(username, password):
    config = get_cognito_configuration()

    response = client.admin_initiate_auth(
        UserPoolId=config["pool"],
        ClientId=config["client"],
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )['AuthenticationResult']

    return response

##############################################################################################
