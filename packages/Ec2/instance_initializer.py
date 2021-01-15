from Cloud.packages.Ec2 import launch_templates_manager, ec2_manager
from Cloud.packages.security import ec2_security_group
from Cloud.packages.network import network_manager
from Cloud.packages.constants import constants
from botocore.exceptions import ClientError
from Cloud.packages import logger
import boto3
import re

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################

def create_instance_handle_from_template(user_id, template_name, security_group_name, subnet_name, instance_profile=""):
    """
    Creates an Ec2 instance with the given parameters parsed on the function.

    This instance will have the name User-user_id to match this with the user using the server

    """

    # client to create the resource Ec2
    client = boto3.resource('ec2')

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
    instance_profile_name = instance_profile if instance_profile else constants.EC2_WORKER_IAM_INSTANCE_PROFILE

    # the state of the instance, will return a dictionary with the instance if exists
    instance = ec2_manager.get_instance_by_tag(value=instance_name)  # None = Instance doesn't not exist
    image_iterator = list(client.images.filter(Owners=[constants.ACCOUNT_ID]))

    if not image_iterator:
        return

    # get the worker image
    images = {}

    for image in image_iterator:
        if image.name.startswith(constants.AMI_NAME):
            images[image.name.split("-")[-1]] = image

    latest_index = max(images.keys())
    image_result = images.get(latest_index)

    if image_result is None:
        log.warning("No AMI found to launch new instance")

    # set the ID for the latest version found
    worker_image_id = image_result.id

    if instance is None:
        try:
            instance = client.create_instances(
                ImageId=worker_image_id,
                IamInstanceProfile={"Name": instance_profile_name},
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

            log.info(f"Instance created: {instance}")

        except ClientError as e:
            log.error(f"Error creating EC2 Instance\nReason: {e.response}")

    else:
        log.warning(f"An Ec2 instance with the name {instance_name} already exist. Operation skipped")

    # to track on cloud watch
    return instance


##############################################################################################
# For test
if __name__ == '__main__':
    create_instance_handle_from_template("0004",
                                         constants.WORKER_LAUNCH_TEMPLATE_NAME,
                                         constants.WORKER_SECURITY_GROUP_NAME,
                                         constants.SUBNET_NAME)
