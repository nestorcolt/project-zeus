from Cloud.packages.iam import iam_manager, policies
from Cloud.packages.constants import constants
import json
import time


##############################################################################################

def iam_boostrap():
    print("************************\nIAM\n************************")

    iam_manager.create_aim_role(constants.EC2_WORKER_IAM_ROLE,
                                description="Manage resources from Ec2 instances",
                                policy_document=json.dumps(policies.ec_role_document))

    iam_manager.create_aim_policy(constants.EC2_TO_SNS_AND_S3_POLICY,
                                  policy_document=policies.s3_and_sns_policy_document,
                                  description="Manage resources from Ec2 instances")

    # attach policy to new role
    ec2_policy_arn = iam_manager.get_policy(constants.EC2_TO_SNS_AND_S3_POLICY, scope="Local")
    iam_manager.attach_role_policy(constants.EC2_WORKER_IAM_ROLE,
                                   policy_arn=ec2_policy_arn["Arn"])

    time.sleep(2)
    print(f"Aim configuration created!")


##############################################################################################

iam_boostrap()
