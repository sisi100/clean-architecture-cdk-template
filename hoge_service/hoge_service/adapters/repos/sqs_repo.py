import json

from boto3.resources.base import ServiceResource

from hoge_service.entities import User


class SqsRepo:
    def __init__(self, resource: ServiceResource, queue_name: str) -> None:
        self.queue = resource.get_queue_by_name(QueueName=queue_name)

    def enqueue_user(self, user: User):
        self.queue.send_message(MessageBody=json.dumps(user.to_dict()))
