from aws_cdk import core
from aws_cdk.aws_dynamodb import Attribute, AttributeType, Table
from aws_cdk.aws_lambda import Code, LayerVersion, Runtime
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_sqs import Queue


class HogeInfraStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ==> DynamoDB
        self.table = Table(
            self,
            "HogeTable",
            partition_key=Attribute(name="pk", type=AttributeType.STRING),
            sort_key=Attribute(name="sk", type=AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        # ==> S3
        self.bucket = Bucket(
            self,
            "HogeBucket",
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        # ==> SQS
        self.queue = Queue(self, "HogeSqs")

        # ==> Lambdalayer
        self.layer = LayerVersion(
            self,
            "aws-lambda-powertools-python-layer",
            compatible_runtimes=[Runtime.PYTHON_3_8],
            code=Code.from_asset("layers/aws-lambda-powertools-python-layer.zip"),
        )
