#libraries
import boto3
import sys
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SQLContext
from pyspark.sql import functions as f
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions

import pandas as pd

class argsGet():
    @property
    def loaded_args(self):
        return self._loaded_args

    def __init__(self, arg_vars=list) -> None:
        self.args = arg_vars
        self._loaded_args= self.load_args()
        pass

    def load_args(self):
        args = getResolvedOptions(sys.argv, self.args)
        return args
        

class CsvToParquet():
    def __init__(self, args) -> None:
        self.args = args 
        #Init Spark Context
        self.sc = SparkContext()
        self.glueContext = GlueContext(self.sc)
        self.logger = self.glueContext.get_logger()
        self.spark = self.glueContext.spark_session
        self.spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic") #to overwrite partitions
        self.job = Job(self.glueContext)
        #Start Spark Job
        self.job.init(self.args['JOB_NAME'], self.args)
        

    def read_data(self):
        self.logger.info("reading csv file into sparkDF")
        sparkDF = self.spark.read.options(header='True', inferSchema='True', delimiter=',').csv("s3://mlops-challenge-rawdata/tables/csv/fe_risk.csv")
        sparkDF.printSchema()
        return sparkDF

    def save_parquet(self, sparkDF):        
        self.logger.info("Repartition and save as parquet")
        sparkDF= sparkDF.withColumn("loan_date", f.from_unixtime(f.unix_timestamp(sparkDF.loan_date), "yyyy-MM-dd"))        
        sparkDF = sparkDF.repartition('loan_date')
        sparkDF.write.mode('overwrite').format('parquet').partitionBy('loan_date').save('s3://mlops-challenge-rawdata/tables/fe_risk/')  

    def main(self):
        sparkDF = self.read_data()        
        self.save_parquet(sparkDF)
        
        self.job.commit()

if __name__ == "__main__":
    """my_args = ['JOB_NAME',
                'day_partition_key',
                'hour_partition_key',
                'day_partition_value',
                'hour_partition_value']"""

    my_args = ['JOB_NAME']
    parser = argsGet(my_args)
    args = parser.loaded_args

    csv_to_parquet = CsvToParquet(args)
    csv_to_parquet.main()