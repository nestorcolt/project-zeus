from Cloud.packages.dynamo import controller, dynamo_manager
from Cloud.packages.constants import constants
import boto3
import time


##############################################################################################

def create_or_update_log(log_group, log_stream, message):
    """
    message will be a python dictionary
    """
    client = boto3.client('logs')

    try:
        client.create_log_group(logGroupName=log_group)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    try:
        client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    response = client.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=log_stream)

    event_log = {
        'logGroupName': log_group,
        'logStreamName': log_stream,
        'logEvents': [
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': message
            }
        ],
    }

    if 'uploadSequenceToken' in response['logStreams'][0]:
        event_log.update({'sequenceToken': response['logStreams'][0]['uploadSequenceToken']})

    response = client.put_log_events(**event_log)
    return response


##############################################################################################
# STATS
def get_user_stats(user_id):
    user_data = dynamo_manager.read_item(constants.USERS_TABLE_NAME, constants.TABLE_PK, user_id)
    offer_list = controller.get_offers(user_id)

    validated_count = len([itm for itm in offer_list if itm["validated"] is True])
    user_block_count = len(controller.get_blocks(user_id))
    user_offer_count = len(offer_list)

    search_state = user_data["search_blocks"]
    last_active = user_data["last_active"]

    # the user state on the search engine
    user_state = "Active"

    if search_state and last_active > controller.get_past_time_span(30):
        user_state = "Stopped"
    if last_active < controller.get_past_time_span(30):
        user_state = "Paused"
    if not search_state:
        user_state = "Inactive"


##############################################################################################
if __name__ == '__main__':
    get_user_stats("15")
