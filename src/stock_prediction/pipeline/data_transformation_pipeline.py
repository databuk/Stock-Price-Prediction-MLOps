
from stock_prediction.config.configuration import ConfigurationManager
from stock_prediction.components.data_transformation import DataTransformation
from stock_prediction import logger

STAGE_NAME = "Data Transformation Pipeline"
class DataTransformationPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(data_transformation_config)
        data_transformation.split_data()
        
if __name__ == "__main__":         
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_transformation_pipeline = DataTransformationPipeline()
        data_transformation_pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e   