import os

import boto3

if os.getenv("IS_LOCAL"):
    local_endpoint = "http://localhost:4566"
    session = boto3.Session(profile_name="localstack")

    DYNAMO_RESOURCE = session.resource("dynamodb", endpoint_url=local_endpoint)
    S3_RESOURCE = session.resource("s3", endpoint_url=local_endpoint)
    SQS_RESOURCE = session.resource("sqs", endpoint_url=local_endpoint)

    TABLE_NAME = "fake-table"
    BUCKET_NAME = "fake-bucket"
    QUEUE_NAME = "fake-queue"
else:
    DYNAMO_RESOURCE = boto3.resource("dynamodb")
    S3_RESOURCE = boto3.resource("s3")
    SQS_RESOURCE = boto3.resource("sqs")

    TABLE_NAME = os.getenv("TABLE_NAME")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    QUEUE_NAME = os.getenv("QUEUE_NAME")
