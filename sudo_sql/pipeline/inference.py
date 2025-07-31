import os
import json
from datetime import datetime
from .base import BasePipeline
from ..models.openai import OpenAIProvider
from ..logger_config import logger
from trl import AutoModelForCausalLMWithValueHead
from transformers import AutoTokenizer

class InferencePipeline(BasePipeline):
    def run(self):
        logger.info("--- Running Inference ---")
        infer_config = self.config['inference']
        output_config = infer_config.get('output', {})
        save_mode = output_config.get('save_mode', 'overwrite')

        output_file = None
        processed_questions = set()
        if output_config.get('save_path'):
            model_name = self.model_config.get("name", "unknown_model").replace("/", "_")
            
            if save_mode == 'resume':
                filename = f"{infer_config['dataset_name']}_{infer_config['split']}_{model_name}.jsonl"
            else:
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                filename = f"{infer_config['dataset_name']}_{infer_config['split']}_{model_name}_{timestamp}.jsonl"
            
            output_file = os.path.join(output_config['save_path'], filename)
            
            if save_mode == 'overwrite' and os.path.exists(output_file):
                os.remove(output_file)
            
            if save_mode == 'resume' and os.path.exists(output_file):
                logger.info(f"Resuming inference run. Loading previously generated results from {output_file}...")
                with open(output_file, 'r') as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            processed_questions.add(data['question'])
                        except json.JSONDecodeError:
                            logger.warning(f"Could not parse line in results file: {line}")
                logger.info(f"Found {len(processed_questions)} previously completed items. Skipping...")

        dataset = self._load_dataset(
            infer_config['dataset_name'], 
            infer_config['data_path'], 
            infer_config['split'], 
            infer_config['schema_type'], 
            infer_config.get('use_cache', True)
        )

        provider_type = self.model_config.get("provider")
        model_name = self.model_config.get("name")

        if provider_type == "openai":
            logger.info(f"Using OpenAI provider with model: {model_name}")
            base_url = self.model_config.get("base_url")
            provider = OpenAIProvider(model=model_name, base_url=base_url)

            for item in dataset:
                if item['question'] in processed_questions:
                    logger.debug(f"Skipping already processed question: {item['question']}")
                    continue

                prompt_text = f"Given the schema: {item['schema']}, generate the SQL for: {item['question']}"
                logger.debug(f"Generating SQL for question: {item['question']}")
                generated_sql = provider.generate(prompt_text)
                logger.info(f"Question: {item['question']}")
                logger.info(f"Generated SQL: {generated_sql}")
                logger.info(f"Ground Truth SQL: {item['sql']}")

                if output_file:
                    result = {
                        "db_id": item['db_id'],
                        "question": item['question'],
                        "generated_sql": generated_sql,
                        "ground_truth_sql": item['sql']
                    }
                    with open(output_file, 'a') as f:
                        f.write(json.dumps(result) + '\n')
        else:
            logger.info(f"Using local Hugging Face model: {model_name}")
            device_map = self.model_config.get('device_map', self.device)
            model = AutoModelForCausalLMWithValueHead.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map=device_map)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            tokenizer.pad_token = tokenizer.eos_token

            for item in dataset:
                if item['question'] in processed_questions:
                    logger.debug(f"Skipping already processed question: {item['question']}")
                    continue

                prompt_text = f"Given the schema: {item['schema']}, generate the SQL for: {item['question']}"
                logger.debug(f"Generating SQL for question: {item['question']}")
                encoded_prompt = tokenizer.encode(prompt_text, return_tensors="pt").to(self.device)
                generated_tokens = model.generate(
                    encoded_prompt,
                    max_new_tokens=self.generation_config.get('max_length', 128),
                )
                generated_sql = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
                logger.info(f"Question: {item['question']}")
                logger.info(f"Generated SQL: {generated_sql}")
                logger.info(f"Ground Truth SQL: {item['sql']}")

                if output_file:
                    result = {
                        "db_id": item['db_id'],
                        "question": item['question'],
                        "generated_sql": generated_sql,
                        "ground_truth_sql": item['sql']
                    }
                    with open(output_file, 'a') as f:
                        f.write(json.dumps(result) + '\n')

        if output_file:
            logger.info(f"Results saved to {output_file}")
        logger.info("--- Inference complete ---")
