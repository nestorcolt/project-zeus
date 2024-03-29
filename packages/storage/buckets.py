from Cloud.packages.constants import constants
from Cloud.packages import logger
import boto3

LOGGER = logger.Logger("S3")
log = LOGGER.logger


##############################################################################################

def create_bucket(name, zone='us-east-1'):
    client = boto3.client("s3")

    try:
        response = client.create_bucket(
            ACL='private',
            Bucket=name,
        )

        log.debug(response)

    except Exception as e:
        log.warning(e)


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
    create_bucket(name=constants.LAMBDA_BUCKET_NAME)
    print("S3 buckets created!")


def dump_buckets_config(buckets_to_dump):
    for itm in buckets_to_dump:
        try:
            delete_bucket(itm)
        except Exception as e:
            log.warning(e)

    print(f"S3 buckets removed: {buckets_to_dump}")

##############################################################################################
