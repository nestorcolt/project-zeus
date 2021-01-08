from constants import constants


def lambda_handler(event, context):
    print(event)
    print(context)

    print("Context members: ")
    print(dir(context))
    print(f"From lambda: {constants.SEARCH_ENGINE_BUCKET_NAME}")
