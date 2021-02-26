from aws_cdk import aws_lambda, core
from aws_cdk.aws_lambda import Code, Function, Tracing

from stacks import HogeInfraStack


class HogeAppStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, infra: HogeInfraStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hoge_service_lambda = Function(
            self,
            "HogeServiceCreateUser",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=Code.from_asset("hoge_service", exclude=["tests"]),
            handler="hoge_service.adapters.handlers.create_user.lambda_handler",
            timeout=core.Duration.seconds(30),
            tracing=Tracing.ACTIVE,
            layers=[infra.layer],
            environment={
                "TABLE_NAME": infra.table.table_name,
                "BUCKET_NAME": infra.bucket.bucket_name,
                "QUEUE_NAME": infra.queue.queue_name,
            },
        )

        infra.table.grant_full_access(hoge_service_lambda)
        infra.bucket.grant_read_write(hoge_service_lambda)
        infra.queue.grant_send_messages(hoge_service_lambda)
