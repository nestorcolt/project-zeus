from botocore.exceptions import ClientError
from modules import logger
from Ec2 import constants
import boto3
import json

LOGGER = logger.Logger(__name__)
log = LOGGER.logger


##############################################################################################

def create_instance_handle():
    # client to create the resource Ec2
    client = boto3.resource('ec2')
    user_id = "4918"

    # response data
    status_code = 200
    instance = []

    try:
        instance = client.create_instances(
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
                'LaunchTemplateId': constants.LAUNCH_TEMPLATE_ID,
                'Version': constants.LAUNCH_TEMPLATE_VERSION
            }
        )

        message = f"Instance created: {instance[0]}"

    except ClientError as e:
        message = f"Error creating EC2 Instance\nReason: {e.response}"
        status_code = 403

    # to track on cloud watch
    log.warning(message)

    return {
        "statusCode": status_code,
        "body": json.dumps({
            "message": message,
        }),
    }


##############################################################################################
create_instance_handle()
