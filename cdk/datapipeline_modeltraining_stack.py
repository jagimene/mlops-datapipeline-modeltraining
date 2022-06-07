from telnetlib import EC
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from .glue_resources import GlueResources
from .ecr_resources import EcrResources

class DatapipelineModeltrainingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config_enviroment:dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.configurations = config_enviroment

    def deploy_glue_resource(self):        
        glue = GlueResources(self, "GlueResources", self.configurations)
        glue.deploy()    
 
    def deploy_ecr_resource(self):
        ecr = EcrResources(self, "EcrResources", self.configurations)
        sm_processing_uri = ecr.uri_img_processing
        sm_training_uri = ecr.uri_img_training

    def deploy(self):        
        # Deploy all the construcs
        self.deploy_glue_resource()
        self.deploy_ecr_resource()
        

       
