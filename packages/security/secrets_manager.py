from botocore.exceptions import ClientError
import base64
import boto3
import json


##############################################################################################

def update_secret(secret_name, data):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')
    client.update_secret(SecretId=secret_name, SecretString=json.dumps(data))


def get_secret(secret_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    return secret

##############################################################################################
