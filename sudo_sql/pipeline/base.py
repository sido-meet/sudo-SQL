from abc import ABC, abstractmethod
import yaml
import torch
from transformers import AutoTokenizer
from trl import AutoModelForCausalLMWithValueHead
from sudo_sql.environments.base import BaseEnvironment
from sudo_sql.data_loaders import get_data_loader
from sudo_sql.logger_config import logger

class BasePipeline(ABC):
    """
    The base class for all pipelines.
    """

    def __init__(self, config: dict):
        """
        Initializes the pipeline from a configuration dictionary.
        """
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_config = self.config['model']
        self.generation_config = self.config.get('generation', {})
        self.training_config = self.config.get('training', {})

    @abstractmethod
    def run(self):
        """
        Runs the pipeline.
        """
        pass

    def _load_dataset(self, dataset_name: str, data_path: str, split: str, schema_type: str, use_cache: bool) -> list[dict]:
        """
        Loads a dataset using the data loader factory.
        """
        loader = get_data_loader(dataset_name, data_path)
        return loader.load_data(split, schema_type, use_cache)

    def _initialize_trainer(self):
        """
        Initializes the model, tokenizer, and PPO trainer.
        """
        from verl import PPOTrainer, PPOConfig

        model_name = self.model_config['name']
        device_map = self.model_config.get('device_map', self.device)

        model = AutoModelForCausalLMWithValueHead.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map=device_map)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token

        ppo_config = PPOConfig(**self.config['ppo'])
        
        return PPOTrainer(
            config=ppo_config,
            model=model,
            tokenizer=tokenizer,
            optimizer_class=torch.optim.AdamW,
        )

    def _train_loop(self, ppo_trainer, env: BaseEnvironment, dataset: list[dict]):
        """
        Runs a generic training loop.
        """
        tokenizer = ppo_trainer.tokenizer
        epochs = self.training_config.get('epochs', 1)
        max_length = self.generation_config.get('max_length', 512)

        for epoch in range(epochs):
            logger.info(f"--- Epoch {epoch + 1}/{epochs} ---")
            for i, item in enumerate(dataset):
                question = item['question']
                schema = item['schema']
                
                prompt_text = f"Given the schema: {schema}, generate the SQL for: {question}"
                encoded_prompt = tokenizer.encode(prompt_text, return_tensors="pt").to(self.device)

                generated_tokens = ppo_trainer.generate(
                    queries=encoded_prompt,
                    gen_len=max_length,
                    batch_size=1,
                )
                
                generated_sql = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
                observation, reward = env.step(generated_sql)

                stats = ppo_trainer.step(
                    queries=[prompt_text],
                    responses=[generated_sql],
                    scores=[torch.tensor(reward)],
                )

                if i % 10 == 0:
                    logger.info(f"Step {i+1}/{len(dataset)} | Reward: {reward:.2f}")
