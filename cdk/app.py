#!/usr/bin/env python3
import os

import aws_cdk as cdk

from datapipeline_modeltraining.pipeline_stack import PipelineStack
from project_environment import ProjectEnvironment


project_enviroment = ProjectEnvironment()
#config_enviroment = project_enviroment.configurations
#print (config_enviroment['stack']['name'], config_enviroment, config_enviroment['pipeline']) #debug
app = cdk.App()
pipeline = PipelineStack(app, project_enviroment.configurations['pipeline']['name'], project_enviroment.configurations['pipeline'])
pipeline.deploy_pipeline()

app.synth()
