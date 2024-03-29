from Cloud.packages.constants import constants
from Cloud.packages import logger
import inspect
import base64
import boto3
import os

LOGGER = logger.Logger("Launch Template Configuration")
log = LOGGER.logger


##############################################################################################

def create_worker_launch_template():
    current_frame = inspect.getfile(inspect.currentframe())
    current_directory = os.path.dirname(current_frame)
    bash_file = os.path.join(current_directory, "Ec2_config.sh")

    # read the bash file with the initial instance configuration
    with open(bash_file, "r") as reader:
        init_script = reader.read()

    # Standard Base64 Encoding
    encoded_bytes = base64.b64encode(init_script.encode("utf-8"))
    encoded_script = str(encoded_bytes, "utf-8")

    # client to create the resource Ec2
    client = boto3.client('ec2')

    response = client.create_launch_template(
        DryRun=False,
        LaunchTemplateName=constants.WORKER_LAUNCH_TEMPLATE_NAME,
        VersionDescription="1",
        LaunchTemplateData={
            'InstanceType': constants.INSTANCE_TYPE,
            'KeyName': constants.KEY_PAIR_NAME,
            'EbsOptimized': True,
            'Monitoring': {
                'Enabled': True
            },
            'DisableApiTermination': False,
            'InstanceInitiatedShutdownBehavior': 'stop',
            'UserData': encoded_script,
        },
        TagSpecifications=[
            {
                'ResourceType': 'launch-template',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': constants.WORKER_LAUNCH_TEMPLATE_NAME
                    },
                ]
            },
        ]
    )

    # log
    log.debug(response)


def remove_launch_templates(launch_templates_to_delete):
    client = boto3.client('ec2')
    launch_templates = client.describe_launch_templates()["LaunchTemplates"]

    if not launch_templates:
        return

    for template in launch_templates:
        template_name = template["LaunchTemplateName"]

        if template_name not in launch_templates_to_delete:
            continue

        try:
            client.delete_launch_template(LaunchTemplateName=template_name)
            log.debug(f"Launch template removed: {template_name}")

        except Exception as e:
            log.exception(e)


def get_worker_launch_template(name):
    client = boto3.client('ec2')
    launch_templates = client.describe_launch_templates()["LaunchTemplates"]

    if not launch_templates:
        return

    for template in launch_templates:
        template_name = template["LaunchTemplateName"]

        if template_name != name:
            continue

        return template

##############################################################################################
