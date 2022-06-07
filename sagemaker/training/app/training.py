import pandas as pd
import argparse
import os, sys
import logging
import json

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, confusion_matrix, precision_score
)
from joblib import dump
from utils import LoggingInit

class Training():
    @property
    def args(self):
        return self._args

    def __init__(self) -> None:
        self.logger = LoggingInit(logging.INFO).logger
        self.logger.info("Init Process")  
        
        self.input_path = '/opt/ml/processing/input'
        self.output_path = '/opt/ml/processing/output'        

        self.input_path = '/home/ch/vscode/ch/repos/mlops-datapipeline-modeltraining/docs/MLOps_Challenge/output'
        self.output_path = '/home/ch/vscode/ch/repos/mlops-datapipeline-modeltraining/docs/MLOps_Challenge/output/model'

        parser = argparse.ArgumentParser()

        parser.add_argument('--model-file', type=str, default='model_risk.joblib')
        parser.add_argument('--model-metrics-file', type=str, default='model_metrics.json')                
        parser.add_argument('--train-data-file', type=str, default='train_data.csv')
        parser.add_argument('--train-target-file', type=str, default='train_target.csv')
        parser.add_argument('--test-data-file', type=str, default='test_data.csv')
        parser.add_argument('--test-target-file', type=str, default='test_target.csv')
        parser.add_argument('--n-estimators', type=int, default=5)

        self._args, _ = parser.parse_known_args()
        self.logger.info("Args loaded")  
        self.logger.info(self._args)  
        
        self.train_data_path = os.path.join(self.input_path, self.args.train_data_file)
        self.train_target_path = os.path.join(self.input_path, self.args.train_target_file)
        self.test_data_path = os.path.join(self.input_path, self.args.test_data_file)
        self.test_target_path = os.path.join(self.input_path, self.args.test_target_file)      
        pass
    
    def load_train_test_data(self):
        X_train = pd.read_csv(self.train_data_path) 
        y_train = pd.read_csv(self.train_target_path)
        X_test = pd.read_csv(self.test_data_path) 
        y_test = pd.read_csv(self.test_target_path) 

        self.logger.info("Loaded data files")
        return (X_train, y_train, X_test, y_test)
    
    def train(self, X_train, y_train, X_test, y_test):
        self.logger.info("Training Started")
        model = RandomForestClassifier(n_estimators = self.args.n_estimators)

        model.fit(X_train, y_train)
        self.logger.info("Training Done")
        y_predict = model.predict(X_test)        
        
        model_metrics = {
            "accuracy_score": accuracy_score(y_test, y_predict),
            "precision_score": precision_score(y_test, y_predict),
            "recall_score": precision_score(y_test, y_predict)
        }

        self.logger.info('Accuracy Score is {:.5}'.format(model_metrics['accuracy_score']))
        self.logger.info('Precision Score is {:.5}'.format(model_metrics['precision_score']))
        self.logger.info('Recall Score is {:.5}'.format(model_metrics['recall_score']))
        self.logger.info(pd.DataFrame(confusion_matrix(y_test,y_predict)))

        return model, model_metrics
    
    def save_model(self, model, model_metrics):
        os.makedirs(self.output_path, exist_ok=True)              
        dump(model, os.path.join(self.output_path, self.args.model_file))
        
        with open(os.path.join(self.output_path, self.args.model_metrics_file), "w") as outfile:
            json.dump(model_metrics, outfile)

        self.logger.info("model and model metrics saved")
        
    
    def main(self):
        #load train test data
        X_train, y_train, X_test, y_test = self.load_train_test_data()
        #train model and get metrics
        model, model_metrics = self.train(X_train, y_train, X_test, y_test)
        #save model artifact and model metrics
        self.save_model(model, model_metrics)


if __name__=='__main__':
    processing = Training()    
    processing.main()