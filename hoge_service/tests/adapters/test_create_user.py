from hoge_service.adapters.handlers.create_user import lambda_handler


def test_handler():
    # MEMO: Mockでないので、本当にローカル環境にデータが入る
    event = {"pk": "12", "name": "テスト太郎", "age": 99}
    lambda_handler(event, None)
