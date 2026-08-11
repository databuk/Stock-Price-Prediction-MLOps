from stock_prediction import logger
from stock_prediction.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from stock_prediction.pipeline.data_validation_pipeline import DataValidationPipeline
from stock_prediction.pipeline.data_transformation_pipeline import DataTransformationPipeline
from stock_prediction.pipeline.model_trainer_pipeline import ModelTrainerPipeline


STAGE_NAME = "Data Ingestion Pipeline"
if __name__ == "__main__":         
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_ingestion_pipeline = DataIngestionPipeline()
        data_ingestion_pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e
    
STAGE_NAME = "Data Validation Pipeline" 
if __name__ == "__main__":         
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_validation_pipeline = DataValidationPipeline()
        data_validation_pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e      
    
STAGE_NAME = "Data Transformation Pipeline"
    
if __name__ == "__main__":         
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_transformation_pipeline = DataTransformationPipeline()
        data_transformation_pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e   
    
STAGE_NAME = "Model Trainer Pipeline"
 
if __name__ == "__main__":         
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        model_trainer_pipeline = ModelTrainerPipeline()
        model_trainer_pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e      
      