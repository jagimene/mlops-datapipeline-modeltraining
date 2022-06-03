from constructs import Construct
from aws_cdk import (
    Stage
)
from .datapipeline_modeltraining_stack import DatapipelineModeltrainingStack
from project_environment import ProjectEnvironment

class PipelineStage(Stage):

    def __init__(self, scope: Construct, id: str, deploy_env:str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.config_enviroment = ProjectEnvironment(deploy_env).configurations
        self.deploy_stack()
        pass


    def deploy_stack(self):
        stack = DatapipelineModeltrainingStack(self, self.config_enviroment['stack']['name']) #Stack app

       