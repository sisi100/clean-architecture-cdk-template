import os

from aws_cdk import core

from stacks import HogeAppStack, HogeInfraStack

app = core.App()
env = core.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="us-east-1")

# Stacks
infra = HogeInfraStack(app, "hoge-infra-stack", env=env)
HogeAppStack(app, "hoge-app-stack", env=env, infra=infra)

app.synth()
