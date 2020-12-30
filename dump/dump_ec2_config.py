import boto3


##############################################################################################
# Ec2 area

def dump_ec2_config():
    client = boto3.client('ec2')
    security_groups = client.describe_security_groups()["SecurityGroups"]

    for group in security_groups:
        name = group["GroupName"]
        try:
            client.delete_security_group(GroupName=name)
        except Exception as e:
            print(e)

    launch_templates = client.describe_launch_templates()["LaunchTemplates"]

    for template in launch_templates:
        name = template["LaunchTemplateName"]
        try:
            client.delete_launch_template(LaunchTemplateName=name)
        except Exception as e:
            print(e)

##############################################################################################
