"""

User IAM managed policies

"""

##############################################################################################
# POLICIES
s3_and_sns_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:*"],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": ["sns:*"],
            "Resource": "*"
        }
    ]
}

##############################################################################################
# ROLES
ec_role_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
        },
    ]
}
