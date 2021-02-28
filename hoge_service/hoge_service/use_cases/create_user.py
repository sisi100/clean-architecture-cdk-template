from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Dict

from hoge_service.entities import User

# ==> I/O


class InputCreateUser(metaclass=ABCMeta):
    @abstractproperty
    def event(self) -> Dict:
        """Eventの取得"""
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user: User) -> None:
        """DBにユーザーを作成する"""
        raise NotImplementedError

    @abstractmethod
    def save_to_storage(self, user: User) -> None:
        """ユーザーをストレージに保存する"""
        raise NotImplementedError

    @abstractmethod
    def enqueue_user(self, user: User) -> None:
        """ユーザーをキューに積む"""
        raise NotImplementedError


class OutputCreateUser(metaclass=ABCMeta):
    @abstractmethod
    def execute(self) -> User:
        """実行する"""
        raise NotImplementedError


# ==> use_case


class CreateUser(OutputCreateUser):
    def __init__(self, use_case_input: InputCreateUser) -> None:
        self._use_case_input = use_case_input

    def execute(self) -> User:

        user = User(**self._use_case_input.event)

        # 何かしらの処理...
        self._use_case_input.create_user(user)
        # 何かしらの処理...
        self._use_case_input.save_to_storage(user)
        # 何かしらの処理...
        self._use_case_input.enqueue_user(user)
        # 何かしらの処理...

        return user
