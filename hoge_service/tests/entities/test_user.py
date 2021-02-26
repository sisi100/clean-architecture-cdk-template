from hoge_service.entities import User


def test_user():
    params = {"pk": "11", "name": "テスト", "age": "99"}
    user = User(**params)
    for key in ["pk", "name", "age"]:
        assert getattr(user, key) == params[key]

    assert user.sk == f'USER#{params["pk"]}'
