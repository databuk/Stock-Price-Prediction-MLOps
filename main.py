from src.stock_prediction import logger
from src.stock_prediction.pipeline.data_ingestion_pipeline import DataIngestionPipeline


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
      