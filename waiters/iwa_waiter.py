from botocore.waiter import create_waiter_with_client
from botocore.exceptions import WaiterError
from botocore.waiter import WaiterModel
import boto3


def internet_gateway_waiter(delay=5, attempts=1):
    client = boto3.client('ec2')
    waiter_name = "internet_gateway_available"

    waiter_config = {
        "version": 2,
        "waiters": {
            waiter_name: {
                "delay": delay,
                "operation": "DescribeInternetGateways",
                "maxAttempts": attempts,
                "acceptors": [
                    {
                        "expected": "available",
                        "matcher": "pathAll",
                        "state": "success",
                        "argument": "InternetGateway[].State"
                    }
                ]
            }
        }
    }

    waiter_model = WaiterModel(waiter_config)
    custom_waiter = create_waiter_with_client(waiter_name=waiter_name,
                                              waiter_model=waiter_model,
                                              client=client)

    try:
        custom_waiter.wait()
        print("Success!!!")

    except WaiterError as e:
        print(e)
