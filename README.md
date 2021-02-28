# clean-architecture-cdk-template

Clean Architecture っぽく CDK でサービスをデプロイするサンプルを作ってみた

## 初期設定

```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

aws-cliのcredentialsにlocalstackのprofileを作る。keyはdummyでOK！
```
[localstack]
aws_access_key_id = dummy
aws_secret_access_key = dummy
```

## ローカルテスト

```
$ make localstack
$ make local_set_up
$ make pytest
```

## デプロイ

```
$ cdk deploy --all
```

