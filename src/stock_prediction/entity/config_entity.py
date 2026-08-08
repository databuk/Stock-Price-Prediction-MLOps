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