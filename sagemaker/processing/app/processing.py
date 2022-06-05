import pandas as pd
import argparse
import os, sys
import logging

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from .utils import LoggingInit

class Processing():
    @property
    def args(self):
        return self._args

    def __init__(self) -> None:
        self.logger = LoggingInit(logging.INFO).logger
        self.logger.info("Init Process")  

        self.input_path = '/opt/ml/processing/input'
        self.output_path = '/opt/ml/processing/output'        

        parser = argparse.ArgumentParser()
        parser.add_argument('--test-size', type=float, default=0.3)
        parser.add_argument('--random-state', type=int, default=123)
        parser.add_argument('--data-file', type=str, default='train_model.csv')
        parser.add_argument('--train-data-file', type=str, default='train_data.csv')
        parser.add_argument('--train-target-file', type=str, default='train_target.csv')
        parser.add_argument('--test-data-file', type=str, default='test_data.csv')
        parser.add_argument('--test-target-file', type=str, default='test_target.csv')
        self._args, _ = parser.parse_known_args()
        self.logger.info("Args loaded")  
        self.logger.info(self._args)  
        
        self.data_path = os.path.join(self.input_path, self.args.data_file) 
        pass
    
    def load_fix_types(self):
        df = pd.read_csv(self.data_path)
        self.logger.info("Loaded df Head ")
        self.logger.info(df.head(5))
        self.logger.info("Loaded df Types ")
        self.logger.info(df.dtypes)

        cust_df = df.copy()
        cust_df.fillna(0, inplace=True)
        return cust_df
    
    def split_train_test(self, cust_df):
        Y = cust_df['status'].astype('int')
        cust_df.drop(['status'], axis=1, inplace=True)
        cust_df.drop(['id'], axis=1, inplace=True)
        X = cust_df

        X_train, X_test, y_train, y_test = train_test_split(X, Y, stratify=Y, 
                                                        test_size = self.args.test_size,
                                                        random_state = self.args.random_state)

        # Using Synthetic Minority Over-Sampling Technique(SMOTE) to overcome sample imbalance problem.
        X_train, y_train = SMOTE().fit_resample(X_train, y_train)
        X_train = pd.DataFrame(X_train, columns=X.columns)

        self.logger.info("X_train Head ")
        self.logger.info(X_train.head(5))

        return (X_train, X_test, y_train, y_test)
    
    def save_split_df(self, X_train, X_test, y_train, y_test):
        os.makedirs(self.output_path, exist_ok=True)        
        X_train.to_csv(os.path.join(self.output_path, self.args.train_data_file), index=False)
        y_train.to_csv(os.path.join(self.output_path, self.args.train_target_file), index=False)
        X_test.to_csv(os.path.join(self.output_path, self.args.test_data_file), index=False)
        y_test.to_csv(os.path.join(self.output_path, self.args.test_target_file), index=False)

        self.logger.info("Preprocessing done")
        
    
    def main(self):
        #load dataset
        cust_df = self.load_fix_types()
        #split data for train and test
        (X_train, X_test, y_train, y_test) = self.split_train_test(cust_df)
        #save training and testing datasets
        self.save_split_df(X_train, X_test, y_train, y_test)


if __name__=='__main__':
    processing = Processing()
    processing.main()