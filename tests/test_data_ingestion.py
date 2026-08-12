import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from stock_prediction.components.data_ingestion import DataIngestion
from stock_prediction.entity.config_entity import DataIngestionConfig

@pytest.fixture
def sample_config(tmp_path):
    data_ingestion_config =  DataIngestionConfig(
        root_dir=tmp_path,
        ticker="AAPL",
        start_date="2020-01-01",
        end_date="2020-01-10",
        raw_data_file=tmp_path / "stock_data.csv",
    )
    return data_ingestion_config
    

@pytest.fixture
def multiindex_dataframe():
    dates = pd.date_range("2026-01-01", periods=3)
    columns = pd.MultiIndex.from_product(
        [["Close", "High", "Low", "Open", "Volume"], ["AAPL"]],
        names=["Price", "Ticker"]
    )
    data = pd.DataFrame(
                [[100, 105, 95, 98, 1000000],
            [101, 106, 96, 99, 1100000],
            [102, 107, 97, 100, 1200000]],
                index=dates, columns=columns
    )

    data.index.name = "Date"
    return data


class TestResetColumns:
    def test_flattens_multiindex(self, sample_config, multiindex_dataframe):
        ingestion = DataIngestion(config=sample_config)
        result = ingestion.reset_columns(multiindex_dataframe)
        assert not isinstance(result.columns, pd.MultiIndex)
        assert list(result.columns) == ["Date", "Close", "High", "Low", "Open", "Volume"]
        
    def test_date_becomes_a_column(self, sample_config, multiindex_dataframe):
        ingestion = DataIngestion(config=sample_config)
        result = ingestion.reset_columns(multiindex_dataframe)
        assert "Date" in result.columns
        assert pd.api.types.is_datetime64_any_dtype(result["Date"])
        
    def test_handles_already_flat_columns(self, sample_config):
        flat_data = pd.DataFrame(
            {"Close": [100], "High": [105], "Low": [95], "Open": [98], "Volume": [1000000]},
            pd.date_range("2026-01-01", periods=1)
        )
        flat_data.index.name = "Date"
        ingestion = DataIngestion(config=sample_config)
        result = ingestion.reset_columns(flat_data)
        assert list(result.columns) == ["Date", "Close", "High", "Low", "Open", "Volume"]
        

class TestFetchFile:
    
    @patch("stock_prediction.components.data_ingestion.yf.download")
    def test_saves_csv_on_successful_download(self, mock_download, sample_config, multiindex_dataframe):
        mock_download.return_value = multiindex_dataframe
        ingestion = DataIngestion(config=sample_config)
        ingestion.fetch_file()
        
        assert sample_config.raw_data_file.exists()
        saved = pd.read_csv(sample_config.raw_data_file)
        assert list(saved.columns) == ["Date", "Close", "High", "Low", "Open", "Volume"]
        assert len(saved) == 3
        
    @patch("stock_prediction.components.data_ingestion.yf.download")     
    def test_raises_on_empty_data(self, mock_download, sample_config):
        mock_download.return_value = pd.DataFrame()
        ingestion = DataIngestion(config=sample_config)
        with pytest.raises(ValueError, match="No data found"):
            ingestion.fetch_file()
        assert not sample_config.raw_data_file.exists()
        
    @patch("stock_prediction.components.data_ingestion.yf.download")            
    def test_raises_on_yfinance_network_error(self, mock_download, sample_config):
        mock_download.side_effect = ConnectionError("network unreachable")
        ingestion = DataIngestion(config=sample_config)
        with pytest.raises(ConnectionError):
            ingestion.fetch_file()
    
  

