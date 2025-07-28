# sudo_sql/training/rl/train_with_verl.py

import argparse
import torch
from transformers import AutoModelForCausalLMWithValueHead, AutoTokenizer
from verl import PPO, PPOTrainer, PPOConfig
from sudo_sql.training.rl.environment import SQLExecutionEnvironment

def main():
    parser = argparse.ArgumentParser(description="Reinforcement Learning with verl for Text-to-SQL")
    
    # Model and tokenizer arguments
    parser.add_argument("--model_name", type=str, default="codellama/CodeLlama-7b-hf", help="The base model to fine-tune.")
    
    # Environment arguments
    parser.add_argument("--db_path", type=str, required=True, help="Path to the SQLite database for the environment.")
    parser.add_argument("--schema", type=str, required=True, help="The schema of the database.")
    parser.add_argument("--question", type=str, required=True, help="A sample question to guide the generation.")

    # PPO arguments
    parser.add_argument("--learning_rate", type=float, default=1.41e-5, help="The learning rate for the PPO optimizer.")
    parser.add_argument("--ppo_epochs", type=int, default=4, help="Number of PPO epochs.")
    parser.add_argument("--batch_size", type=int, default=256, help="PPO batch size.")

    args = parser.parse_args()

    # 1. Initialize Environment
    env = SQLExecutionEnvironment(db_path=args.db_path)

    # 2. Load Model and Tokenizer
    # Note: verl works best with a model that has a value head for PPO.
    # We use AutoModelForCausalLMWithValueHead for this.
    model = AutoModelForCausalLMWithValueHead.from_pretrained(args.model_name, torch_dtype=torch.bfloat16, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.pad_token = tokenizer.eos_token

    # 3. Configure PPO
    config = PPOConfig(
        p_learning_rate=args.learning_rate,
        v_learning_rate=args.learning_rate,
        ppo_epochs=args.ppo_epochs,
        batch_size=args.batch_size,
    )
    
    # 4. Create PPO Trainer
    ppo_trainer = PPOTrainer(
        config=config,
        model=model,
        tokenizer=tokenizer,
        optimizer_class=torch.optim.AdamW,
    )

    # 5. Prepare the generation prompt
    prompt_text = f"Given the schema: {args.schema}, generate the SQL for: {args.question}"
    encoded_prompt = tokenizer.encode(prompt_text, return_tensors="pt").to(model.device)

    # 6. Generate a batch of SQL queries
    generated_tokens = ppo_trainer.generate(
        queries=encoded_prompt,
        gen_len=100, # Max length of the generated SQL
        batch_size=args.batch_size,
    )
    
    # Decode the generated tokens into text
    generated_sql_list = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

    # 7. Get rewards from the environment
    rewards = []
    for sql in generated_sql_list:
        _, reward = env.step(sql)
        rewards.append(torch.tensor(reward))

    # 8. Run PPO step
    stats = ppo_trainer.step(
        queries=[prompt_text] * len(generated_sql_list),
        responses=generated_sql_list,
        scores=rewards,
    )

    print("PPO step finished.")
    print(f"Stats: {stats}")

    # In a real scenario, you would loop steps 6-8 for many iterations.
    # Here we just show one step for demonstration.

if __name__ == "__main__":
    main()
