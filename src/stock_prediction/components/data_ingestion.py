import yfinance as yf
from stock_prediction import logger
import pandas as pd
from stock_prediction.entity.config_entity import DataIngestionConfig
from stock_prediction.utils.common import save_csv

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config =  config
    
    def fetch_file(self):
        try:
            
            logger.info(f"Data downloading for ticker: {self.config.ticker} from \
                {self.config.start_date} to {self.config.end_date}")
            data = yf.download(
                tickers=self.config.ticker,
                start=self.config.start_date,
                end=self.config.end_date
            )
            logger.info(f"Data downloaded successfully for ticker: {self.config.ticker} from \
                {self.config.start_date} to {self.config.end_date}")
            if not (data.empty):
                data = self._preprocesss(data)          
                save_csv(data, self.config.raw_data_file)

            else:
                logger.error(f"Empty data found for ticker: {self.config.ticker} from \
                    {self.config.start_date} to {self.config.end_date}") 
                raise ValueError(f"Empty data found for ticker: {self.config.ticker} from \
                    {self.config.start_date} to {self.config.end_date}")
        except Exception as e:
            logger.error(f"Error while downloading data for ticker: {self.config.ticker} ")
            raise e

        
        
    def _preprocesss(self, data: pd.DataFrame) -> pd.DataFrame:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
        data = data.reset_index()
        # data = pd.read_csv(data, parse_dates="Date")
        data.columns = data.columns.str.lower() 
        return data