from Cloud.packages import logger
import boto3
import json

LOGGER = logger.Logger("DynamoDB")
log = LOGGER.logger


##############################################################################################

def get_table_by_name(table_name):
    client = boto3.resource("dynamodb").Table(table_name)
    return client


def create_item(table_name, dictionary_item):
    table = get_table_by_name(table_name)

    try:
        table.put_item(Item=dictionary_item)
    except Exception as e:
        log.error(e)


def read_item(table_name, field, value):
    table = get_table_by_name(table_name)
    resp = table.get_item(
        Key={
            field: value,
        }
    )

    if 'Item' in resp:
        return resp['Item']

    return None


def update_item(table_name, dictionary_item):
    pass


def delete_item(table_name, primary_key, value):
    table = get_table_by_name(table_name)

    try:
        table.delete_item(
            Key={
                primary_key: value,
            },
        )
    except Exception as e:
        log.error(e)


##############################################################################################
if __name__ == '__main__':
    read_item("Users", "user_id", 55)
