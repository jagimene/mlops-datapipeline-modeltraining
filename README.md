# MLOps-Solution
Pipeline for Feature Engineering and Model Training with CI/CD Pipeline

The main purpose of this challenge is to assess your skills (1) building a scalable
data pipeline for feature engineering & training machine learning model using good CI/CD
practices (2) creating an API to serve those features, and (3) creating a prediction service
that uses the created features.

This solution was focused in leverage the codes that can create features from a file and create a model building an 
Scalable MLOps Solution.

Solutions Architecture 
======================================================
![Solutions Architecture](docs/architecture/MLOps.drawio.png?width=60pc) 

There are 3 (Dev Prod CI/CD) accounts represented here, can be more, but its a simple example of Enviroment Replication. Dev - Test - PreProd - Prod, etc.

To the rigth there is a CI/CD pipeline, that its conected to Github as a code versioning resource. An AWS Pipeline is connected to the branch and is the responsable to deploy the stack.



## CI/CD Pipeline Stack
======================================================  
The pipeline is connected to the repo changes, deploy the stacks, build the images, create the bucket, lambdas, database, etc
It has a **Manual approval Step** to promote from Dev Environment to Test Environment

![code pipeline](docs/img/deploy_testing.JPG?width=60pc) 
![code pipeline](docs/img/manual_approval.JPG?width=60pc) 
![code pipeline](docs/img/manual_approval2.JPG?width=60pc) 


## ML Data Train Stack
======================================================


**ML Database**: Stores the Features Tables for MLTeam  
**Data Bucket**: Stores csv data and parquet   
**Artifact Bucket**: Stores model trained and code  
**ECR Repo**: Stores Docker Images for Training and Preprocessing  
**CloudWatch**: Stores Logs for monitoring and debug

**AWS Step Function Workflow**

- **Data Pipeline**  
Glue Shell Job Read Data From a Raw/Staging source in csv  
Glue Spark Job Transform it to parquet file to store it in ML DB  
Glue Crawler Creates / Updates Table in Glue Data Catalog
- **ML Training Pipeline**  
Sagemker Preporcess Data (clean, transform, etc)  
Sagemaker Model Training, creates a model generates an artifac (joblib) and model metrics file for analysis (json) 
![Step Function](docs/img/step_function_pipeline.png?width=10pc) 
## API Serving Stack
======================================================


**ECR Repo**: Stores Docker Images for Lambdas Features And Model Serving  
**CloudWatch**: Stores Logs for monitoring and debug

- **Api Features**  
Api Features a Lambda process the data and connects to MLDB Table, an ApiWategay provides a Rest connection  

- **ML Training Pipeline**  
Api Model Serving a Lambda process the prediction connects to Api Features and get the model trained artifact. An ApiWategay provides a Rest connection  
Glue Crawler Creates / Updates Table in Glue Data Catalog

Repo Structure
======================================================

The Code is splitted in two repos. Each one with a CI/CD pipeline Stack, config yml for environments definitions.

## [Data Pipeline and Model training](https://github.com/jagimene/mlops-datapipeline-modeltraining)  

Repo Structure
```
.
├── README.md                       
├── __init__.py
├── app.py                                  #cdk Entrypoint
├── cdk
│   ├── README.md
│   ├── __init__.py
│   ├── config                              #cdk config for each environment
│   │   ├── default.yml
│   │   ├── dev.yml
│   │   └── prod.yml
│   ├── datapipeline_modeltraining_stack.py #stack
│   ├── ecr_resources.py                    #cdk construcs
│   ├── glue_resources.py                   #cdk construcs
│   ├── pipeline_stack.py                   #cdk construcs
│   ├── pipeline_stage.py                   #cdk construcs
│   └── project_environment.py              #class for get configs from ymls
├── cdk.json
├── docs                                    #Docs Folder
│   ├── MLOps_Challenge
│   │   ├── MLE_challenge - Features engineering - Notebook 1.ipynb
│   │   ├── MLE_challenge - Training model - Notebook 2.ipynb
│   ├── architecture                        
│   │   └── MLOps.drawio.png
│   └── img
│       ├── deploy_testing.JPG
├── glue                                    #Glue
│   ├── fe_risk.py                          #Glue Job Shell
│   ├── fe_to_parquet.py                    #Glue Job Spark
├── sagemaker   
│   ├── processing                          #PreprocessData app (Docker)
│   │   ├── Dockerfile
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   ├── processing.py
│   │   │   └── utils.py
│   │   └── requirements.txt
│   ├── requirements-dev.txt
│   ├── requirements.txt
│   └── training                            #Training app (Docker)
│       ├── Dockerfile
│       ├── app
│       │   ├── __init__.py
│       │   ├── training.py
│       │   └── utils.py
│       └── requirements.txt
├── stepfunction                            #Data Pipeline and Model Training
│   ├── data_model_pipeline_payload.json
│   └── mlops-data-modeltraining-dev_data_pipeline.asl.json
└── tests
    ├── __init__.py
    └── unit
        ├── __init__.py
        └── test_datapipeline_modeltraining_stack.py
```


## [API Features and Model Serving](https://github.com/jagimene/mlops-api-serving)  

Repo Structure
```
.
├── README.md
├── app.py
├── cdk                                  #cdk Entrypoint
│   ├── README.md
│   ├── __init__.py
│   ├── api_serving_features.py         #cdk construcs
│   ├── api_serving_model.py            #cdk construcs
│   ├── config                          #cdk config for each environment
│   │   ├── default.yml
│   │   ├── dev.yml
│   │   └── prod.yml
│   ├── mlops_api_serving_stack.py      #Stack
│   ├── pipeline_stack.py               #cdk construcs
│   ├── pipeline_stage.py               #cdk construcs
│   └── project_environment.py          #class for get configs from ymls
├── cdk.json
├── docs                                #docs
│   └── img
│       ├── cdk_deploy_pipeline_end.JPG
├── lambdas                             #Lambdas
│   ├── serving_features                #Features lambda (Docker)
│   │   ├── Dockerfile
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   ├── serving_features.py
│   │   │   ├── sql
│   │   │   │   └── get_features.sql
│   │   │   └── utils.py
│   │   └── requirements.txt
│   └── serving_model                   #Model Serving lambda (Docker)
│       ├── Dockerfile
│       ├── app
│       │   ├── __init__.py
│       │   ├── serving_model.py
│       │   └── utils.py
│       └── requirements.txt
└── tests
    ├── __init__.py
    └── unit
        ├── __init__.py
        └── test_mlops_api_serving_stack.py
```
Test APIs
======================================================
The APIs can be testing.

## [Api Model Serving](https://7otjwyncgg.execute-api.us-east-1.amazonaws.com/prod/predict/) 
```
curl https://7otjwyncgg.execute-api.us-east-1.amazonaws.com/prod/predict/?user_id=5137035

{"id": "5137035", "prediction": 0}

--
curl https://7otjwyncgg.execute-api.us-east-1.amazonaws.com/prod/predict/?test

{"msg": "Test Success"}
```
## [Api Features Serving](https://7otjwyncgg.execute-api.us-east-1.amazonaws.com/prod/predict/) 
```
curl https://7p622wr07a.execute-api.us-east-1.amazonaws.com/prod/features/?user_id=5021985

{"age": 31, "years_on_the_job": 12, "nb_previous_loans": 9, "avg_amount_loans_previous": 153.1254538753544, "flag_own_car": 1}

--
curl https://7p622wr07a.execute-api.us-east-1.amazonaws.com/prod/features/?test

{"msg": "Test Success"}
```

Real Life Use Case
======================================================
## QA 
Serveral QA checks, Features and Monitoring can be implemented bettwen each step, from Data Quality (rows, columns, format, datatypes, etc). Model Drift Analysis Model Metrics and Model Performance. Alarms, etc.

Here are some ideas.

## Code
- Add more comments Docstrings for easy to reuse and share code.
## Handle Errors and Exeptions
- Improve handling in expected an unexpedted error, for better usability
## Add Testing 
- Local testing. Before push to repo
- CDK Infractructure Testing
- CI Pipelines. Develop unit testing for each feature
- CD Pipelines. Integral Testing before production
- Prod Testing 2 releases, Canary deployments, A/B Testing, etc

## Add ML Model Registry
- As Source Versining of new releases of the model.

## API
- Improve security with token
- Improve delay changing the architecture, add dynamo table for features for ex.

## Monitoring
- Add Monitoring tools and features for all the architecture, Cloud Watch Alarms for example.
