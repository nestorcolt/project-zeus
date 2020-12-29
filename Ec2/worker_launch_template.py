from constants import constants
import boto3
import inspect
import base64
import os


def create_launch_template():
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
        LaunchTemplateName=constants.LAUNCH_TEMPLATE_NAME,
        VersionDescription=constants.LAUNCH_TEMPLATE_VERSION,
        LaunchTemplateData={
            'EbsOptimized': True,
            'ImageId': constants.AMI_ID,
            'Monitoring': {
                'Enabled': True
            },
            'DisableApiTermination': False,
            'InstanceInitiatedShutdownBehavior': 'stop',
            'UserData': encoded_script,
            'SecurityGroups': [
                constants.WORKER_SECURITY_GROUP_NAME,
            ],
        },
        TagSpecifications=[
            {
                'ResourceType': 'launch-template',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': constants.LAUNCH_TEMPLATE_NAME
                    },
                ]
            },
        ]
    )

    # log
    print(response)

##############################################################################################
