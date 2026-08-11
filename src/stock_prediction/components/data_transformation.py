from stock_prediction.entity.config_entity import DataTransformationConfig
from stock_prediction import logger
import pandas as pd
import os

class DataTransformation:
    def __init__(self, config:DataTransformationConfig):
        self.config = config
    def split_data(self):
        data = pd.read_csv(self.config.raw_data_file)
        data = data.set_index(self.config.date_column)
        data = data[self.config.target_column]
        train_size = int(len(data) * self.config.test_size)
        train_data = data[:train_size]
        test_data = data[train_size:]
        
        assert train_data.index.max() < test_data.index.min(), \
            "Data leakage detected, train/test split overlap"
        logger.info(f"Train date range:{train_data.index.min()} to {train_data.index.max()}")
        logger.info(f"Test date range: {test_data.index.min()} to {test_data.index.max()}")
        train_data.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=True)
        test_data.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=True)

        return train_data, test_data
        
        
        