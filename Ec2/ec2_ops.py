from Ec2 import constants
import pprint
import boto3
import json

INSTANCE_ID = "i-0a497d3cc7a58b2a8"


##############################################################################################

def get_all_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    return response


def get_instance_by_tag(key="Name", value="0000", add_tags=None):
    if add_tags is None:
        add_tags = {}
    ec2 = boto3.client('ec2')

    custom_filter = [
        {
            'Name': f'tag:{key}',
            'Values': [value]
        }
    ]

    if add_tags:
        custom_filter = add_tags

    response = ec2.describe_instances(Filters=custom_filter)
    return response


def start_instance_handle():
    ec2 = boto3.client('ec2')

    # response data
    status_code = 200
    instance_ids = [INSTANCE_ID]

    # Dry run succeeded, run start_instances without dry run
    try:
        ec2.start_instances(InstanceIds=instance_ids, DryRun=False)
        message = f"Instance started: {instance_ids}"

    except Exception as e:
        message = f"Error starting EC2 Instance\nReason: {e}"
        status_code = 403

    # to track on cloud watch
    print(message)

    return {
        "statusCode": status_code,
        "body": json.dumps({
            "message": message,
        }),
    }


def stop_instance_handle():
    # client to create the resource Ec2
    client = boto3.resource('ec2')

    # response data
    status_code = 200
    instance_ids = [INSTANCE_ID]

    try:
        client.instances.filter(InstanceIds=instance_ids).stop()
        message = f"Instance stopped: {instance_ids}"

    except Exception as e:
        message = f"Error stopping EC2 Instance\nReason: {e}"
        status_code = 403

    # to track on cloud watch
    print(message)

    return {
        "statusCode": status_code,
        "body": json.dumps({
            "message": message,
        }),
    }


def delete_instance_handle():
    # client to create the resource Ec2
    client = boto3.resource('ec2')

    # response data
    status_code = 200
    instance_ids = [INSTANCE_ID]

    try:
        client.instances.filter(InstanceIds=instance_ids).terminate()
        message = f"Instance deleted: {instance_ids}"

    except Exception as e:
        message = f"Error deleting EC2 Instance\nReason: {e}"
        status_code = 403

    # to track on cloud watch
    print(message)

    return {
        "statusCode": status_code,
        "body": json.dumps({
            "message": message,
        }),
    }

##############################################################################################
