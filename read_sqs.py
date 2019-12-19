import boto3
import datetime
import os
import json
from get_info import get_info


def endpoint(event, context):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=str(os.environ['SQS']))

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(str(os.environ['S3']))
    body = []
    proxy = {'https': str(os.environ['PROXY'])}

    for message in queue.receive_messages(MaxNumberOfMessages=2):
        try:
            info = get_info(url=message.body, proxy=proxy)
            info["url"] = message.body
            s3_body = json.dumps(info)
            key = f"{message.body}|{datetime.datetime.utcnow()}.json".replace("/", "|")
            bucket.put_object(Key=key, Body=s3_body)
        except Exception as e:
            body.append({"url": message.body, "state": False, "error": repr(e)})
        else:
            body.append({"url": message.body, "state": True})
        finally:
            message.delete()

    response = {
        "statusCode": 200,
        "body": body
    }

    return response
