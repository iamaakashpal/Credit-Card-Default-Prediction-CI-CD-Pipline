from creditcarddefault.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,\
ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig,TrainingPipelineConfig
import os,sys
from creditcarddefault.logger import logging
from creditcarddefault.exception import CreditException
from creditcarddefault.util.util import read_yaml_file
from creditcarddefault.constant import *

class Configuartion: # Visit example_configuration.ipynb file for Explaination
    def __init__(self,config_file_path:str = CONFIG_FILE_PATH,current_time_stamp:str = CURRENT_TIME_STAMP) -> None:
        self.config_info = read_yaml_file(file_path = config_file_path)
        self.training_pipeline_config = self.get_training_pipeline_config()
        self.time_stamp = current_time_stamp

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        pass

    def get_data_validation_config(self) -> DataValidationConfig:
        pass

    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY] # training_pipeline_config: pipeline_name: creditcarddefault artifact_dir: artifact
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])

            training_pipeline_config = TrainingPipelineConfig(artifact_dir = artifact_dir)
            logging.info(f"Training Pipeline config:{training_pipeline_config}")
            return training_pipeline_config


        except Exception as e:
            raise CreditException(e,sys) from e