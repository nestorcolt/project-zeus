from Cloud.packages import logger
import boto3

LOGGER = logger.Logger("Ec2")
log = LOGGER.logger


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


def check_instance_state(name):
    instances = get_instance_by_tag(value=name)["Reservations"]
    statuses = []

    if not instances:
        return None

    client = boto3.client('ec2')

    for itm in instances:
        ami = itm["Instances"][0]
        instance_id = ami["InstanceId"]
        response = client.describe_instance_status(InstanceIds=[instance_id])['InstanceStatuses']

        if not response:
            statuses.append("inactive")
            continue

        status = response[0]['InstanceState']['Name']

        if status == "running":
            statuses.append("active")

    return statuses


def start_instance_handle(name):
    ec2 = boto3.client('ec2')
    instance = get_instance_by_tag(value=name)["Reservations"]

    if not instance:
        return

    ami = instance[0]["Instances"][0]
    instance_id = ami["InstanceId"]

    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        message = f"Instance started: {instance_id}"

    except Exception as e:
        message = f"Error starting EC2 Instance\nReason: {e}"

    # to track on cloud watch
    log.warning(message)


def stop_instance_handle(name):
    # client to create the resource Ec2
    client = boto3.resource('ec2')
    instance = get_instance_by_tag(value=name)["Reservations"]

    if not instance:
        return

    ami = instance[0]["Instances"][0]
    instance_id = ami["InstanceId"]

    try:
        client.instances.filter(InstanceIds=[instance_id]).stop()
        message = f"Instance stopped: {instance_id}"

    except Exception as e:
        message = f"Error stopping EC2 Instance\nReason: {e}"

    # to track on cloud watch
    log.warning(message)


def delete_instance_handle(name):
    # client to create the resource Ec2
    client = boto3.resource('ec2')
    instance = get_instance_by_tag(value=name)["Reservations"]

    if not instance:
        return

    ami = instance[0]["Instances"][0]
    instance_id = ami["InstanceId"]

    try:
        client.instances.filter(InstanceIds=[instance_id]).terminate()
        message = f"Instance deleted: {instance_id}"

    except Exception as e:
        message = f"Error deleting EC2 Instance\nReason: {e}"

    # to track on cloud watch
    log.warning(message)

##############################################################################################
