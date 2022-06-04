#libraries
import boto3, logging, sys
import sys
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
from awsglue.utils import getResolvedOptions
import pandas as pd
import s3fs #s3fs-0.4.2

class LoggingInit():
    @property
    def logger(self):
        return self._logger

    def __init__(self, level=logging.DEBUG, msg_format= '%(asctime)s %(levelname)s %(name)s: %(message)s', date_format= '%Y-%m-%d %H:%M:%S') -> None:
        self.msg_format = msg_format
        self.date_format = date_format
        self.level = level            
        self._logger=self.set_logging()
        pass
    
    def set_logging(self):
        logging.basicConfig(format=self.msg_format, datefmt=self.date_format, stream=sys.stdout)
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(sys.stdout))#for glue job
        logger.setLevel(self.level)
        logger.info("Logger Initializated")
        return (logger)


class ArgsGet():
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
        

class FeRisk():
    def __init__(self, args) -> None:
        self.args = args 
        self.logger = LoggingInit(logging.INFO).logger
        self.logger.info("info message")
        self.logger.warn("warn message")
        self.logger.error("error message")
        pass

    def read_data(self):
        self.logger.info("loading csv file")
        df = pd.read_csv('s3://mlops-challenge-rawdata/dataset_credit_risk.csv')
        shape = df.shape
        print(shape)
        self.logger.info("load success")
        return df
    
    def preprocess(self, df):
        self.logger.info("start proprocessing")
        df = df.sort_values(by=["id", "loan_date"])
        df = df.reset_index(drop=True)
        df["loan_date"] = pd.to_datetime(df.loan_date)
        print(df.head(2))
        self.logger.info("end proprocessing")
        return df

    def features_calculation(self, df):
        self.logger.info("Feature nb_previous_loans")
        df_grouped = df.groupby("id")
        df["nb_previous_loans"] = df_grouped["loan_date"].rank(method="first") - 1

        self.logger.info("Feature avg_amount_loans_previous")
        df['avg_amount_loans_previous'] = (
        df.groupby('id')['loan_amount'].apply(lambda x: x.shift().expanding().mean()))

        self.logger.info("Feature age")
        df['birthday'] = pd.to_datetime(df['birthday'], errors='coerce')
        df['age'] = (pd.to_datetime('today').normalize() - df['birthday']).dt.days // 365

        self.logger.info("Feature years_on_the_job")
        df['job_start_date'] = pd.to_datetime(df['job_start_date'], errors='coerce')
        df['years_on_the_job'] = (pd.to_datetime('today').normalize() - df['job_start_date']).dt.days // 365
        
        self.logger.info("Feature flag_own_car")
        df['flag_own_car'] = df.flag_own_car.apply(lambda x : 0 if x == 'N' else 1)

        df.head(2)
        return df

    def save_features(self, df):
        self.logger.info("Store all data to process later and save as parquet")
        df.to_csv('s3://mlops-challenge-rawdata/tables/csv/fe_risk.csv', index=False)

        self.logger.info("Store data for training model csv")
        df = df[['id', 'age', 'years_on_the_job', 'nb_previous_loans', 'avg_amount_loans_previous', 'flag_own_car', 'status']]
        df.to_csv('s3://mlops-challenge-rawdata/train_model.csv', index=False)
        pass

    def main(self):
        df = self.read_data()
        df = self.preprocess(df)
        df = self.features_calculation(df)
        self.save_features(df)        
        

if __name__ == "__main__":
    """my_args = ['JOB_NAME',
                'day_partition_key',
                'hour_partition_key',
                'day_partition_value',
                'hour_partition_value']"""

    my_args = ['JOB_NAME']
    parser = ArgsGet(my_args)
    args = parser.loaded_args

    features = FeRisk(args)
    features.main()