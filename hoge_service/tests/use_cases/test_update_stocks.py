import boto3

from hoge_service.entities import User
from hoge_service.use_cases import CreateUser, InputCreateUser, OutputCreateUser

# ==> O/I


class Input(InputCreateUser):
    def create_user(self, user: User):
        return True

    def save_to_storage(self, user: User):
        return True

    def enqueue_user(self, user: User):
        return True


class Output(OutputCreateUser):
    def result(self, user: User):
        return user


# ==> handler


def test_use_case():

    event = {"pk": "12", "name": "テスト太郎", "age": 99}

    use_case = CreateUser(input_=Input(), output=Output())
    result = use_case.execute(event)

    assert User(**event).to_dict() == result.to_dict()
