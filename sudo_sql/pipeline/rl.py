from .base import BasePipeline
from ..environments.sql_execution import SQLExecutionEnvironment
from ..logger_config import logger

class RLPipeline(BasePipeline):
    def run(self):
        logger.info("--- Running RL ---")
        rl_config = self.config['rl']
        env = SQLExecutionEnvironment(db_path=rl_config['db_path'])
        ppo_trainer = self._initialize_trainer()
        rl_dataset = [{'question': rl_config['question'], 'schema': rl_config['schema'], 'sql': ''}] * self.training_config.get('steps', 100)
        self._train_loop(ppo_trainer, env, rl_dataset)
        logger.info("--- RL complete ---")
        output_dir = self.training_config.get('output_dir')
        if output_dir:
            logger.info(f"Saving model to {output_dir}...")
            ppo_trainer.save_model(output_dir)
            logger.info("Model saved.")
