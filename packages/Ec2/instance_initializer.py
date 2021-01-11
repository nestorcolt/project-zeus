from Cloud.packages.Ec2 import launch_templates_manager, ec2_manager
from Cloud.packages.security import ec2_security_group
from Cloud.packages.network import network_manager
from botocore.exceptions import ClientError
from Cloud.packages import logger
import boto3

LOGGER = logger.Logger("Instance Creation")
log = LOGGER.logger


##############################################################################################

def create_instance_handle_from_template(user_id, template_name, security_group_name, subnet_name):
    """
    Creates an Ec2 instance with the given parameters parsed on the function.

    This instance will have the name User-user_id to match this with the user using the server

    """

    # client to create the resource Ec2
    client = boto3.client('ec2')

    template = launch_templates_manager.get_worker_launch_template(template_name)
    security_group = ec2_security_group.get_security_group_by_name(security_group_name)
    subnet = network_manager.subnet_exist_check(subnet_name)

    if not template:
        log.error("No valid launch template found. Operation aborted!")
        return

    elif not security_group:
        log.error("No valid security group found. Operation aborted!")
        return

    elif not subnet:
        log.error("No valid subnet found. Operation aborted!")
        return

    # response data
    instance_name = f'User-{user_id}'
    instance = None

    # the state of the instance, will return a dictionary with the instance if exists
    instance = ec2_manager.get_instance_by_tag(instance_name)  # None = Instance doesn't not exist

    if instance is not None:
        log.warning(f"An Ec2 instance with the name {instance_name} already exist. Operation skipped")
        return instance

    try:
        instance = client.run_instances(
            MaxCount=1,
            MinCount=1,
            SubnetId=subnet["SubnetId"],
            SecurityGroupIds=[
                security_group["GroupId"],
            ],
            Monitoring={'Enabled': True},
            DisableApiTermination=False,
            InstanceInitiatedShutdownBehavior='stop',
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'client',
                            'Value': user_id
                        },
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ],
            LaunchTemplate={
                'LaunchTemplateId': template["LaunchTemplateId"],
                'Version': str(template["LatestVersionNumber"])
            }
        )

        message = f"Instance created: {instance}"

    except ClientError as e:
        message = f"Error creating EC2 Instance\nReason: {e.response}"

    # to track on cloud watch
    log.warning(message)
    return instance

##############################################################################################
