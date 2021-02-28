from typing import Dict

from hoge_service.entities import User
from hoge_service.use_cases import CreateUser, InputCreateUser


class MockInput(InputCreateUser):
    def __init__(self, event: Dict) -> None:
        self._event = event

    @property
    def event(self) -> Dict:
        return self._event

    def create_user(self, user: User) -> None:
        return

    def save_to_storage(self, user: User) -> None:
        return

    def enqueue_user(self, user: User) -> None:
        return


# ==> handler


def test_use_case():

    event = {"pk": "12", "name": "テスト太郎", "age": 99}
    use_case = CreateUser(MockInput(event))
    assert User(**event) == use_case.execute()
