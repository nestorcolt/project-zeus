from botocore.waiter import create_waiter_with_client
from botocore.exceptions import WaiterError
from botocore.waiter import WaiterModel
import boto3


##############################################################################################

def internet_gateway_waiter(gateway_id, delay=10, attempts=2):
    waiter_name = "internet_gateway_available"
    client = boto3.client('ec2')

    waiter_config = {
        "version": 2,
        "waiters": {
            waiter_name: {
                "delay": delay,
                "operation": "DescribeInternetGateways",
                "maxAttempts": attempts,
                "acceptors": [
                    {
                        "expected": gateway_id,
                        "matcher": "pathAny",
                        "state": "success",
                        "argument": f"InternetGateways[].InternetGatewayId"
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

    except WaiterError as e:
        print(e)

##############################################################################################
