import os
from typing import Dict

import boto3
from aws_lambda_powertools import Logger, Tracer

from hoge_service.adapters.repos import DynamoDbRepo, S3Repo, SqsRepo
from hoge_service.entities import User
from hoge_service.use_cases import CreateUser, InputCreateUser, OutputCreateUser

logger = Logger()
tracer = Tracer()

# ==> I/O


class Input(InputCreateUser):
    def __init__(self, db_repo: DynamoDbRepo, storage_repo: S3Repo, queue_repo: SqsRepo) -> None:
        self.db_repo = db_repo
        self.storage_repo = storage_repo
        self.queue_repo = queue_repo

    def create_user(self, user: User):
        return self.db_repo.create_user(user)

    def save_to_storage(self, user: User):
        return self.storage_repo.put_user(user, key=user.sk)

    def enqueue_user(self, user: User):
        return self.queue_repo.enqueue_user(user)


class Output(OutputCreateUser):
    def result(self, user: User):
        return user.to_dict()


# ==> handler


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: Dict, context):
    """
    ハンドラーのサンプル

    Lambdaをける方法がないので、Lambdaのコンソールからeventを入れてけってみる。
    eventの例(↓)
    ```
    event={"pk": "12", "name":"テスト太郎", "age": 99}
    ```
    """

    dynamo_resource = boto3.resource("dynamodb")
    s3_resource = boto3.resource("s3")
    sqs_resource = boto3.resource("sqs")

    table_name = os.getenv("TABLE_NAME")
    bucket_name = os.getenv("BUCKET_NAME")
    queue_name = os.getenv("QUEUE_NAME")

    input_ = Input(
        db_repo=DynamoDbRepo(dynamo_resource, table_name),
        storage_repo=S3Repo(s3_resource, bucket_name),
        queue_repo=SqsRepo(sqs_resource, queue_name),
    )
    output = Output()

    use_case = CreateUser(input_=input_, output=output)
    return use_case.execute(event)
