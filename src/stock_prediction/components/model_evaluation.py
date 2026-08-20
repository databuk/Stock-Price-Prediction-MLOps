
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from stock_prediction.utils.common import *
import mlflow
from urllib.parse import urlparse
from stock_prediction.entity.config_entity import ModelEvaluationConfig
from mlflow import MlflowClient


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
        
        mlflow.set_experiment("stock-arima-prediction")

        tracking_uri_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        
        with mlflow.start_run():
            predictions = arima_result.forecast(len(test_data))
            (rmse, mae, r2) = self._eval_metrics(test_data, predictions)
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(Path(self.config.metric_file_path), scores)
            mlflow.log_param("order", self.config.params)
            mlflow.log_metrics(metrics=scores)
            
            registered_model_name = "arima_model" if tracking_uri_type_store !="file" else None
            model_info = mlflow.statsmodels.log_model(arima_result, name="model", registered_model_name=registered_model_name)
            self._promote_if_better(
                registered_model_name, model_info.registered_model_version,
                rmse,
            )
    
    def _promote_if_better(self, model_name: str, new_version:str, new_rmse: float, alias: str="champion"):
        client = MlflowClient()
        try:
            current_champion = client.get_model_version_by_alias(model_name, alias)
            current_run = client.get_run(current_champion.run_id)
            current_rmse = current_run.data.metrics.get("rmse")
        except:
            current_champion = None
            current_rmse = None
        if current_champion is None or current_rmse is None or new_rmse < current_rmse:
            client.set_registered_model_alias(model_name, alias, new_version)
            logger.info(
                f"Promoted {model_name}_v{new_version} (rmse={new_rmse:.3f}) to alias '{alias}'" 
                 + (f", replacing rmse={current_rmse:.3f}" if current_rmse is not None else '(first champion)')
                
           )
        else:
            logger.info(
                f"{model_name} v{new_version} (rmse={new_rmse:.3f}) did not beat current "
                f"champion (rmse={current_rmse:.3f}) - champion unchanged"
            )
            
