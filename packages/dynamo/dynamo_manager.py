from string import ascii_lowercase
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

    try:
        resp = table.get_item(
            Key={
                field: value,
            }
        )

        if 'Item' in resp:
            return resp['Item']

    except Exception as e:
        log.error(e)

    return None


def map_expression_attributes_values(dictionary_item):
    expression_template = "set "
    result_dict = {}

    for index, (key, values) in enumerate(dictionary_item.items()):
        key_name = f":{ascii_lowercase[index]}"
        expression_template = expression_template + f"{key} = {key_name}, "
        result_dict[key_name] = values

    return expression_template[:-2], result_dict


def update_item(table_name, primary_key, value, items):
    expression_key, expression_values = map_expression_attributes_values(items)
    table = get_table_by_name(table_name)

    table.update_item(
        Key={
            primary_key: value,
        },
        UpdateExpression=expression_key,
        ExpressionAttributeValues=expression_values,
        ReturnValues="UPDATED_NEW"
    )


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
    data = {"search_blocks": False}
    update_item("Users", "user_id", 55, data)
