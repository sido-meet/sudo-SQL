# sudo_sql/training/sft/train.py

import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig
from trl import SFTTrainer
from sudo_sql.training.sft.data_processor import load_and_prepare_dataset

def train():
    parser = argparse.ArgumentParser(description="Supervised Fine-Tuning with LoRA")
    
    # Model and tokenizer arguments
    parser.add_argument("--model_name", type=str, default="codellama/CodeLlama-7b-hf", help="The base model to fine-tune.")
    
    # Data arguments
    parser.add_argument("--dataset_name", type=str, default="b-mc2/sql-create-context", help="The dataset to use for training.")
    
    # LoRA arguments
    parser.add_argument("--lora_r", type=int, default=8, help="The rank of the LoRA matrices.")
    parser.add_argument("--lora_alpha", type=int, default=16, help="The alpha parameter for LoRA.")
    parser.add_argument("--lora_dropout", type=float, default=0.1, help="The dropout probability for LoRA.")
    
    # Training arguments
    parser.add_argument("--output_dir", type=str, default="./sft-output", help="The directory to save the trained model.")
    parser.add_argument("--num_train_epochs", type=int, default=1, help="Number of training epochs.")
    parser.add_argument("--per_device_train_batch_size", type=int, default=4, help="Batch size per device during training.")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1, help="Number of updates steps to accumulate before performing a backward/update pass.")
    parser.add_argument("--learning_rate", type=float, default=2e-4, help="The initial learning rate.")
    
    args = parser.parse_args()

    # 1. Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.pad_token = tokenizer.eos_token # Set pad token for padding
    
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=torch.bfloat16, # Use bfloat16 for efficiency
        device_map="auto"
    )

    # 2. Load and prepare dataset
    train_dataset = load_and_prepare_dataset(args.dataset_name, tokenizer)

    # 3. Configure LoRA
    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj"] # Target attention layers
    )

    # 4. Configure Training Arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        logging_dir=f"{args.output_dir}/logs",
        logging_steps=10,
        save_steps=100,
        fp16=False, # bfloat16 is preferred if available
        bf16=True,
    )

    # 5. Initialize SFTTrainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        peft_config=peft_config,
        dataset_text_field="text", # We need to tell the trainer which field contains our formatted text
        max_seq_length=512,
        tokenizer=tokenizer,
        args=training_args,
    )

    # 6. Start training
    print("Starting Supervised Fine-Tuning...")
    trainer.train()
    print("Training complete.")

    # 7. Save the final model
    final_model_path = f"{args.output_dir}/final"
    trainer.save_model(final_model_path)
    print(f"Model saved to {final_model_path}")

if __name__ == "__main__":
    train()
