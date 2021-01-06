import boto3

client = boto3.client('sns')

response = client.create_topic(
    Name='string',
    Attributes={
        'string': 'string'
    },
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ]
)
