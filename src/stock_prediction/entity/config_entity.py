from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    raw_data_file: Path
    ticker: str
    start_date: str
    end_date: str
    
    
    