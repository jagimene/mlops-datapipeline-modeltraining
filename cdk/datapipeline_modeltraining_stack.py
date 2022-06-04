from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from .glue_resources import GlueResources

class DatapipelineModeltrainingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config_enviroment:dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.configurations = config_enviroment

    def deploy_glue_resource(self):
        glue = GlueResources(self, "GlueResources", self.configurations)
        glue.deploy()

    def deploy(self):
        self.deploy_glue_resource()
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "DatapipelineModeltrainingQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
