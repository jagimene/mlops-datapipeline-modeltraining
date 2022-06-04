from aws_cdk import (
    Aws,
    aws_iam as iam,
    aws_glue as glue,
    aws_s3 as s3,    
)  
account = Aws.ACCOUNT_ID
from constructs import Construct  

class GlueResources(Construct):
    def __init__(self, scope: Construct, id: str, configurations: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.configurations = configurations
        self.project_name = self.configurations['projectName']
        

    def create_buckets(self):
        
        bucket_name_artifact = self.configurations['glue']['bucket_artifact']['name']
        bucket_name_data = self.configurations['glue']['bucket_data']['name']

        bucket_artifact = s3.Bucket(self, 
                            f"{self.project_name }_{bucket_name_artifact}", 
                            versioned=False, 
                            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        arn_bucket_artifact = bucket_artifact.bucket_arn
        
        bucket_data = s3.Bucket(self, 
                            f"{self.project_name }_{bucket_name_data}", 
                            versioned=False, 
                            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        arn_bucket_data = bucket_data.bucket_arn

        return (arn_bucket_artifact, arn_bucket_data, bucket_data)

    def create_db(self):
        db_name = self.configurations['glue']['database_ml']['name']

        ml_db = glue.CfnDatabase(
            self,
            id=db_name,
            catalog_id=account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                description=f"Glue database '{self.project_name}_{db_name}'",
                name=db_name,
            )
        )

    def create_glue_role(self):
        write_to_s3_policy = iam.PolicyDocument(
        statements=[iam.PolicyStatement(
            actions=["s3:GetObject","s3:PutObject"],                
            resources=[self._arn_bucket_artifact, self._arn_bucket_artifact]
            )] )              

        role = iam.Role(
            self, f"GlueCrawlerRole",
            role_name = f"{self.project_name }_gluecrawler_role",
            inline_policies=[write_to_s3_policy],
            assumed_by=iam.ServicePrincipal('glue.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSGlueServiceRole')]
        )
        return role
    
    def create_glue_crawler(self):
        crawler_name = self.configurations['glue']['crawler_features']['name']
        database_name = self.configurations['glue']['database_ml']['name']
        bucket_name = self._bucket_data.bucket_name
        prefix = self.configurations['glue']['crawler_features']['s3Path']
        
        create_gule_crawler = glue.CfnCrawler(
            self, f'glue-crawler-{crawler_name}',
            description=f"Glue Crawler for {database_name} {crawler_name}",
            name=f'{crawler_name}',
            database_name=database_name,
            #schedule={"scheduleExpression": "cron(5 * * * ? *)"},
            role=self._glue_crawler_role.role_arn,
            targets={"s3Targets": [{"path": f"s3://{bucket_name}/{prefix}"}]}, 
            schema_change_policy={"DeleteBehavior": "DELETE_FROM_DATABASE", "UpdateBehavior": "UPDATE_IN_DATABASE"}
        )
    
    def deploy(self):
        self._arn_bucket_artifact, self._arn_bucket_data, self._bucket_data= self.create_buckets()
        self._glue_crawler_role = self.create_glue_role()
        self.create_db()
        self.create_glue_crawler()