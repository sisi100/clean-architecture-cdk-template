from typing import Dict

from aws_lambda_powertools import Logger, Tracer

from hoge_service.adapters.repos import DynamoDbRepo, S3Repo, SqsRepo
from hoge_service.entities import User
from hoge_service.settings import BUCKET_NAME, DYNAMO_RESOURCE, QUEUE_NAME, S3_RESOURCE, SQS_RESOURCE, TABLE_NAME
from hoge_service.use_cases import CreateUser, InputCreateUser, OutputCreateUser

# ==> I/O


class Input(InputCreateUser):
    def __init__(self, event: Dict, db_repo: DynamoDbRepo, storage_repo: S3Repo, queue_repo: SqsRepo) -> None:
        self._db_repo = db_repo
        self._storage_repo = storage_repo
        self._queue_repo = queue_repo
        self._event = event

    @property
    def event(self):
        return self._event

    def create_user(self, user: User):
        return self._db_repo.create_user(user)

    def save_to_storage(self, user: User):
        return self._storage_repo.put_user(user, key=user.sk)

    def enqueue_user(self, user: User):
        return self._queue_repo.enqueue_user(user)


class Presenter:
    def __init__(self, use_case_output: OutputCreateUser) -> None:
        self._use_case_output = use_case_output

    def result(self) -> Dict:
        user = self._use_case_output.execute()
        return user.to_dict()


# ==> handler


logger = Logger()
tracer = Tracer()


# @logger.inject_lambda_context(log_event=True)
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
    return Presenter(
        CreateUser(
            Input(
                event=event,
                db_repo=DynamoDbRepo(DYNAMO_RESOURCE, TABLE_NAME),
                storage_repo=S3Repo(S3_RESOURCE, BUCKET_NAME),
                queue_repo=SqsRepo(SQS_RESOURCE, QUEUE_NAME),
            )
        )
    ).result()
