from abc import ABCMeta, abstractmethod
from typing import Dict

from hoge_service.entities import User


class InputCreateUser(metaclass=ABCMeta):
    @abstractmethod
    def create_user(self, user: User):
        """DBにユーザーを作成する"""
        raise NotImplementedError

    @abstractmethod
    def save_to_storage(self, user: User):
        """ユーザーをストレージに保存する"""
        raise NotImplementedError

    @abstractmethod
    def enqueue_user(self, user: User):
        """ユーザーをキューに積む"""
        raise NotImplementedError


class OutputCreateUser(metaclass=ABCMeta):
    @abstractmethod
    def result(self, user: User):
        raise NotImplementedError


# ==> use_case


class CreateUser:
    def __init__(self, input_: InputCreateUser, output: OutputCreateUser) -> None:
        self.input_ = input_
        self.output = output

    def execute(self, event: Dict):

        user = User(**event)

        self.input_.create_user(user)
        # 何かしらの処理...
        self.input_.save_to_storage(user)
        # 何かしらの処理...
        self.input_.enqueue_user(user)
        # 何かしらの処理...

        return self.output.result(user)
