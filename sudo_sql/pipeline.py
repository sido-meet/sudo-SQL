import yaml
import torch
from transformers import AutoTokenizer
from trl import AutoModelForCausalLMWithValueHead
from sudo_sql.environments.base import BaseEnvironment
from sudo_sql.environments.sft import SFTEnvironment
from sudo_sql.environments.sql_execution import SQLExecutionEnvironment
from sudo_sql.models.openai import OpenAIProvider
from sudo_sql.data_loaders import get_data_loader

class UnifiedPipeline:
    """
    The core unified pipeline for all operations.
    """

    def __init__(self, config_path: str):
        """
        Initializes the pipeline from a configuration file.
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_config = self.config['model']
        self.generation_config = self.config.get('generation', {})
        self.training_config = self.config.get('training', {})

    def run(self):
        """
        Runs the pipeline based on the loaded configuration.
        """
        mode = self.config.get("mode")
        if mode == "sft":
            self._run_sft()
        elif mode == "rl":
            self._run_rl()
        elif mode == "infer":
            self._run_inference()
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def _load_dataset(self, dataset_name: str, data_path: str, split: str) -> list[dict]:
        """
        Loads a dataset using the data loader factory.
        """
        loader = get_data_loader(dataset_name, data_path)
        return loader.load_data(split)

    def _initialize_trainer(self):
        """
        Initializes the model, tokenizer, and PPO trainer.
        """
        # Moved verl imports here to avoid issues when not training
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
            print(f"--- Epoch {epoch + 1}/{epochs} ---")
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
                    print(f"Step {i+1}/{len(dataset)} | Reward: {reward:.2f}")

    def _run_sft(self):
        """
        Runs the Supervised Fine-Tuning (SFT) process.
        """
        print("--- Running SFT ---")
        sft_config = self.config['sft']
        dataset = self._load_dataset(sft_config['dataset_name'], sft_config['data_path'], 'train')
        env = SFTEnvironment(dataset)
        ppo_trainer = self._initialize_trainer()
        self._train_loop(ppo_trainer, env, dataset)
        print("--- SFT complete ---")
        output_dir = self.training_config.get('output_dir')
        if output_dir:
            print(f"Saving model to {output_dir}...")
            ppo_trainer.save_model(output_dir)
            print("Model saved.")

    def _run_rl(self):
        """
        Runs the Reinforcement Learning (RL) process.
        """
        print("--- Running RL ---")
        rl_config = self.config['rl']
        env = SQLExecutionEnvironment(db_path=rl_config['db_path'])
        ppo_trainer = self._initialize_trainer()
        rl_dataset = [{'question': rl_config['question'], 'schema': rl_config['schema'], 'sql': ''}] * self.training_config.get('steps', 100)
        self._train_loop(ppo_trainer, env, rl_dataset)
        print("--- RL complete ---")
        output_dir = self.training_config.get('output_dir')
        if output_dir:
            print(f"Saving model to {output_dir}...")
            ppo_trainer.save_model(output_dir)
            print("Model saved.")

    def _run_inference(self):
        """
        Runs the inference process on a dataset.
        """
        print("--- Running Inference ---")
        infer_config = self.config['inference']
        dataset = self._load_dataset(infer_config['dataset_name'], infer_config['data_path'], infer_config['split'])

        provider_type = self.model_config.get("provider")
        model_name = self.model_config.get("name")

        if provider_type == "openai":
            print(f"Using OpenAI provider with model: {model_name}")
            base_url = self.model_config.get("base_url")
            provider = OpenAIProvider(model=model_name, base_url=base_url)

            for item in dataset:
                prompt_text = f"Given the schema: {item['schema']}, generate the SQL for: {item['question']}"
                generated_sql = provider.generate(prompt_text)
                print(f"\nQuestion: {item['question']}")
                print(f"Generated SQL: {generated_sql}")
                print(f"Ground Truth SQL: {item['sql']}")
        else:
            # Local model inference remains the same, but now iterates through the dataset
            print(f"Using local Hugging Face model: {model_name}")
            device_map = self.model_config.get('device_map', self.device)
            model = AutoModelForCausalLMWithValueHead.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map=device_map)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            tokenizer.pad_token = tokenizer.eos_token

            for item in dataset:
                prompt_text = f"Given the schema: {item['schema']}, generate the SQL for: {item['question']}"
                encoded_prompt = tokenizer.encode(prompt_text, return_tensors="pt").to(self.device)
                generated_tokens = model.generate(
                    encoded_prompt,
                    max_new_tokens=self.generation_config.get('max_length', 128),
                )
                generated_sql = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
                print(f"\nQuestion: {item['question']}")
                print(f"Generated SQL: {generated_sql}")
                print(f"Ground Truth SQL: {item['sql']}")

        print("\n--- Inference complete ---")