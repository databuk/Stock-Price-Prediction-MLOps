from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    raw_data_file: Path
    ticker: str
    start_date: str
    end_date: str
    

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    raw_data_file: Path
    status_file: Path
    ge_expectation_suite: str
    all_schema: dict
    
    
@dataclass()
class DataTransformationConfig:
    root_dir: Path
    raw_data_file: Path
    split_date: str
    target_column: str
    date_column: str
    


@dataclass()
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    target_column: str
    date_column: str
    model_name: str
    order: list
 
@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metric_file_path: Path
    date_column: str
    params: list
    mlflow_tracking_uri: str
    
    
    