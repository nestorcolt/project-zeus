from Cloud.packages.Ec2 import launch_templates_manager
from Cloud.packages.network import network_manager
from Cloud.packages.security import ec2_security_group
from Cloud.packages.constants import constants
from botocore.exceptions import ClientError
from Cloud.packages import logger
import boto3

LOGGER = logger.Logger("Instance Creation")
log = LOGGER.logger


##############################################################################################

def create_instance_handle_from_template(user_id, template_name, security_group_name, subnet_name):
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
    instance = None

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
                            'Value': f'User-{user_id}'
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

create_instance_handle_from_template("4110",
                                     constants.WORKER_LAUNCH_TEMPLATE_NAME,
                                     constants.WORKER_SECURITY_GROUP_NAME,
                                     constants.SUBNET_NAME)
