import boto3
import datetime
import os
import json


def endpoint(event, context):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=str(os.environ['SQS']))

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(str(os.environ['S3']))
    body = []

    for message in queue.receive_messages(MaxNumberOfMessages=10):
        try:
            if str(message.body).startswith("http"):
                raise ValueError("input url")
            s3_body = json.dumps({"url": message.body, "titile": "title"})
            bucket.put_object(Key=f"{message.body}|{datetime.datetime.utcnow()}", Body=s3_body)
        except Exception:
            body.append({"url": message.body, "state": 0})
        else:
            body.append({"url": message.body, "state": 1})
        finally:
            message.delete()

    response = {
        "statusCode": 200,
        "body": body
    }

    return response
