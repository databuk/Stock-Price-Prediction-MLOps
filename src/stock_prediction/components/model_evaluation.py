
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from stock_prediction.utils.common import *
import mlflow
from urllib.parse import urlparse
from stock_prediction.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
    def _eval_metrics(self, actual, pred):
        rmse = root_mean_squared_error(actual, pred)
        mae =  mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    def log_into_mlflow(self):
        test_data = pd.read_csv(self.config.test_data_path)
        test_data = test_data.set_index(self.config.date_column)
        arima_result = load_bin(Path(self.config.model_path))
        #mlflow.set_registry_uri(self.config.mlflow_uri)
  
        mlflow.set_tracking_uri(self.config.mlflow_tracking_uri)
        
        mlflow.set_experiment("stock-arima-forcasting")

        tracking_uri_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        
        with mlflow.start_run():
            predictions = arima_result.forecast(len(test_data))
            (rmse, mae, r2) = self._eval_metrics(test_data, predictions)
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(Path(self.config.metric_file_path), scores)
            mlflow.log_param("order", self.config.params)
            mlflow.log_metrics(metrics=scores)
            
            if tracking_uri_type_store != "file":
                mlflow.statsmodels.log_model(arima_result, name="model", registered_model_name="Arima_model")
            else:
                mlflow.statsmodels.log_model(arima_result, name="model")
        
        
        
        