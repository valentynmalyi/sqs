import os
import boto3



def endpoint(event, context):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=str(os.environ['SQS']))

    body = []

    for url in event:
        res = queue.send_message(MessageBody=str(url))
        body.append(res)

    response = {
        "statusCode": 200,
        "body": body
    }

    return response
