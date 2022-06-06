from aws_cdk import (
    Aws,
    Duration,
    CfnOutput,
    aws_iam as iam,
    aws_ecr as ecr,
    aws_ecr_assets as ecrass,
    
)  
account = Aws.ACCOUNT_ID
from constructs import Construct  

class EcrResources(Construct):
    @property
    def uri_img_training(self):
        return self._uri_img_training

    @property
    def uri_img_processing(self):
        return self._uri_img_processing

    def __init__(self, scope: Construct, id: str, configurations: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.configurations = configurations
        self.project_name = self.configurations['projectName']
        self._deploy()
        

    def _create_ecr_repo(self):
        name = f"{self.project_name}_{self.configurations['ecr']['repo']['name']}"
        lifecycle_days = self.configurations['ecr']['repo']['lifecycle_days']
        tag_exclude = self.configurations['ecr']['repo']['tag_exclude']

        repo = ecr.Repository(self,
                                id='ModelRepo',
                                repository_name=name,
                                lifecycle_rules=[
                                    ecr.LifecycleRule.max_image_age(Duration.days(lifecycle_days),
                                    ecr.LifecycleRule.tag_prefix_list(tag_exclude),
                                )]
                            )
        return repo
    
    def _build_image(self):
        processing_name = f"{self.project_name}_{self.configurations['ecr']['asset']['sm_processing']['name']}"
        processing_path = self.configurations['ecr']['asset']['sm_processing']['path']

        
        training_name = f"{self.project_name}_{self.configurations['ecr']['asset']['sm_training']['name']}"
        training_path = self.configurations['ecr']['asset']['sm_training']['path']

        processing_img = ecrass.DockerImageAsset(self, 
                                processing_name,
                                directory=processing_path
                                )

        training_img = ecrass.DockerImageAsset(self, 
                                training_name,
                                directory=training_path
                                )

        CfnOutput( #get uri in output cloudformation stack
            self, f"{processing_name}_uri",
            value = processing_img.image_uri
        )

        CfnOutput( #get uri in output cloudformation stack
            self, f"{training_name}_uri",
            value = training_img.image_uri
        )

        return processing_img, training_img
    
    
    def _deploy(self):
        self._repo= self.create_ecr_repo()
        self._processing_img, self._training_img = self.build_image()
        self._uri_img_processing = self._processing_img.image_uri
        self._uri_img_training = self._training_img.image_uri