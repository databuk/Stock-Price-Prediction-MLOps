import os
import importlib
from datetime import datetime
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG



PROJECT_ROOT =  "/opt/airflow/project"

def run_stage(pipeline_module, pipeline_class_name):
    os.chdir(PROJECT_ROOT)
    module = importlib.import_module(pipeline_module)
    pipeline_class = getattr(module, pipeline_class_name)
    pipeline_class().main()

with DAG(
    dag_id="stock_prediction_pipeline",
    start_date=datetime(2026, 8, 14, 16, 0, 0),
    schedule=None,
    catchup=False,
) as dag:
    
    
    data_ingestion = PythonOperator(
        task_id="data_ingestion",
        python_callable=run_stage,
        op_kwargs={
            "pipeline_module": "stock_prediction.pipeline.data_ingestion_pipeline",
            "pipeline_class_name": "DataIngestionPipeline"
        }
        
    )
    
    data_validation = PythonOperator(
        task_id="data_validation",
        python_callable=run_stage,
        op_kwargs={
            "pipeline_module": "stock_prediction.pipeline.data_validation_pipeline",
            "pipeline_class_name": "DataValidationPipeline"
        }
        
    )
    
    data_transformation = PythonOperator(
        task_id="data_transformation",
        python_callable=run_stage,
        op_kwargs={
            "pipeline_module": "stock_prediction.pipeline.data_transformation_pipeline",
            "pipeline_class_name": "DataTransformationPipeline"
        }    
    )
    
    model_trainer = PythonOperator(
        task_id="model_trainer",
        python_callable=run_stage,
        op_kwargs={
            "pipeline_module": "stock_prediction.pipeline.model_trainer_pipeline",
            "pipeline_class_name": "ModelTrainerPipeline"
        }
        
    )
    
    model_evaluation = PythonOperator(
        task_id="model_evaluation",
        python_callable=run_stage,
        op_kwargs={
            "pipeline_module": "stock_prediction.pipeline.model_evaluation_pipeline",
            "pipeline_class_name": "ModelEvaluationPipeline"
        }
        
    )
    data_ingestion >> data_validation >> data_transformation >> model_trainer >> model_evaluation


 