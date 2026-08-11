from stock_prediction.constants import *
from src.stock_prediction.utils.common import *
from src.stock_prediction.entity.config_entity import *


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
            test_size=config.test_size,
            target_column=config.target_column,
            date_column=config.date_column
        )
        return data_transformation_config