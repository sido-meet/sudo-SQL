from .base import BasePipeline
from ..environments.sft import SFTEnvironment
from ..logger_config import logger

class SFTPipeline(BasePipeline):
    def run(self):
        logger.info("--- Running SFT ---")
        sft_config = self.config['sft']
        dataset = self._load_dataset(
            sft_config['dataset_name'], 
            sft_config['data_path'], 
            'train', 
            sft_config['schema_type'], 
            sft_config.get('use_cache', True)
        )
        env = SFTEnvironment(dataset)
        ppo_trainer = self._initialize_trainer()
        self._train_loop(ppo_trainer, env, dataset)
        logger.info("--- SFT complete ---")
        output_dir = self.training_config.get('output_dir')
        if output_dir:
            logger.info(f"Saving model to {output_dir}...")
            ppo_trainer.save_model(output_dir)
            logger.info("Model saved.")
