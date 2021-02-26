import json

from boto3.resources.base import ServiceResource

from hoge_service.entities import User


class S3Repo:
    def __init__(self, resource: ServiceResource, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.resource = resource

    def put_user(self, user: User, key: str) -> None:
        object = self.resource.Object(self.bucket_name, key)
        object.put(Body=json.dumps(user.to_dict()).encode("UTF-8"))
