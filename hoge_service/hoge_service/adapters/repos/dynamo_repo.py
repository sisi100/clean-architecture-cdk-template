from boto3.resources.base import ServiceResource

from hoge_service.entities import User


class DynamoDbRepo:
    def __init__(self, resource: ServiceResource, table_name: str) -> None:
        self.table = resource.Table(table_name)

    def create_user(self, user: User):
        self.table.put_item(Item=user.to_dict())
