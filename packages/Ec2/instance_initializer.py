from Cloud.packages.Ec2 import launch_templates_manager
from Cloud.packages.constants import constants
from botocore.exceptions import ClientError
from Cloud.packages import logger
import boto3

LOGGER = logger.Logger("Instance Creation")
log = LOGGER.logger


##############################################################################################

def create_instance_handle_from_template(user_id, template_name):
    # client to create the resource Ec2
    client = boto3.client('ec2')

    template = launch_templates_manager.get_worker_launch_template(name=template_name)

    if not template:
        log.error("No valid launch template found. Operation aborted!")
        return

    # response data
    instance = []

    try:
        instance = client.run_instances(
            MaxCount=1,
            MinCount=1,
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

        message = f"Instance created: {instance[0]}"

    except ClientError as e:
        message = f"Error creating EC2 Instance\nReason: {e.response}"

    # to track on cloud watch
    log.warning(message)
    return instance


##############################################################################################

create_instance_handle_from_template("4110", constants.WORKER_LAUNCH_TEMPLATE_NAME)
