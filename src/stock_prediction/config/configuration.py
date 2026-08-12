from stock_prediction.constants import *
from stock_prediction.utils.common import *
from stock_prediction.entity.config_entity import *
import os
from dotenv import load_dotenv
mlflow_tracking_uri = load_dotenv("MLFLOW_TRACKING_URI")


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, schema_filepath=SCHEMA_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            raw_data_file=Path(config.raw_data_file),
            ticker=config.ticker,
            start_date=config.start_date,
            end_date=config.end_date
        )
        return data_ingestion_config
    
    def get_data_validation_config(self):
        config = self.config.data_validation
        schema = self.schema.columns
        create_directories([config.root_dir])
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            raw_data_file=Path(config.raw_data_file),
            status_file=Path(config.status_file),
            ge_expectation_suite=config.ge_expectation_suite,
            all_schema=schema
        )
        return data_validation_config

    def get_data_transformation_config(self):
        config = self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config =  DataTransformationConfig(
            root_dir=config.root_dir,
            raw_data_file=config.raw_data_file,
            split_date=config.split_date,
            target_column=config.target_column,
            date_column=config.date_column
        )
        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer

        create_directories([config.root_dir])
        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            model_name=config.model_name,
            date_column=self.schema.date_column,
            target_column=self.schema.target_column.name,
            order=self.params.ARIMA.order
            
        )
        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        create_directories([config.root_dir])
        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            model_path=config.model_path,
            metric_file_path=config.metric_file_path,
            params=self.params.ARIMA.order,
            date_column=self.schema.date_column,
            mlflow_tracking_uri=config.mlflow_tracking_uri
            
        )
        return model_evaluation_config