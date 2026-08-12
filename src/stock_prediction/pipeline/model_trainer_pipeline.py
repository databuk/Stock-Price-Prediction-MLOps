from stock_prediction import logger
from stock_prediction.config.configuration import ConfigurationManager
from stock_prediction.components.model_trainer import ModelTrainer

STAGE_NAME = "Model Training Pipeline"

class ModelTrainerPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(model_trainer_config)
        model_trainer.train()
        
if __name__ == "__main__":         
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_trainer_pipeline = ModelTrainerPipeline()
        data_trainer_pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e      