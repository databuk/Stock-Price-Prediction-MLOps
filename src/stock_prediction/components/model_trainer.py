import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from stock_prediction import logger
from stock_prediction.utils.common import *


class ModelTrainer:
    def __init__(self, config):
      self.config = config
    def train(self) -> ARIMA:
      train_df = pd.read_csv(self.config.train_data_path, parse_dates=[self.config.date_column])
      
      train = train_df.set_index(self.config.date_column)[self.config.target_column]
  
      arima_model = ARIMA(train, order=self.config.order)
      logger.info("Model training complete")
      # arima_model.fit()
      model_path =  Path(self.config.root_dir) / self.config.model_name
      save_bin(arima_model, model_path)
      logger.info(f"Arima model saved to {model_path}")
      return arima_model
      
    
    