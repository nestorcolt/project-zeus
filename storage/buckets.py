from constants import constants
from modules import logger
import boto3

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


def create_bucket(name, zone='eu-west-1'):
    client = boto3.client("s3")

    try:
        response = client.create_bucket(
            ACL='private',
            Bucket=name,
            CreateBucketConfiguration={
                'LocationConstraint': zone,
            },
        )

        log.debug(response)

    except Exception as e:
        log.exception(e)


def get_bucket_by_name(name):
    client = boto3.client("s3")
    response = client.list_buckets()

    for itm in response["Buckets"]:
        if itm["Name"] == name:
            return itm


def delete_bucket(name):
    client = boto3.client("s3")
    bucket = get_bucket_by_name(name)

    if not bucket:
        return

    try:
        response = client.delete_bucket(
            Bucket=name,
        )
        log.debug(response)

    except Exception as e:
        log.exception(e)


def configure_software_bucket():
    print("************************\nS3\n************************")
    create_bucket(name=constants.SEARCH_ENGINE_BUCKET_NAME)
    print("S3 buckets created!")

##############################################################################################
