def lambda_handler(event, context):
    print(event)
    print(context)

    print("Context members: ")
    print(dir(context))
