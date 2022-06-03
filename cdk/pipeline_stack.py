from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines
)
from .pipeline_stage import PipelineStage

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, config_pipeline: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        self.config_enviroment = config_pipeline            
       
    #Create base pipeline
    def deploy_pipeline(self):
        config_pipeline = self.config_enviroment
        pipeline_name = config_pipeline['name']
        github_owner = config_pipeline['github']['owner']
        github_repo = config_pipeline['github']['repo']
        github_branch = config_pipeline['github']['branch']
        
        pipeline =  pipelines.CodePipeline(
                    self, "Pipeline", 
                    pipeline_name=pipeline_name,
                    synth=pipelines.ShellStep("Synth", #Synyh pipeline
                        input=pipelines.CodePipelineSource.git_hub(f"{github_owner}/{github_repo}", github_branch),
                        commands=[
                            "npm install -g aws-cdk", # Installs the cdk cli on Codebuild
                            "cd cdk",
                            "python -m pip install -r requirements.txt", # Install required packages
                            "cdk synth", #python                            
                        ]
                    )
                )

        dev_stage = PipelineStage(self, "Deploy-Dev", "dev")
        prod_stage = PipelineStage(self, "Deploy-Prod", "prod")

        deploy_dev = pipeline.add_stage(dev_stage) #stage deploy
        deploy_prod = pipeline.add_stage(prod_stage)        
        
        deploy_dev.add_post(
            pipelines.ManualApprovalStep("PromoteToProd")
        )