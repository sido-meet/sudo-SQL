# sudo_sql/training/sft/data_processor.py

from datasets import load_dataset

def format_prompt(sample):
    """
    Formats a sample into a structured prompt for training.
    This function creates a standardized instruction-following format.
    """
    return f"""<s>[INST] Given the database schema: {sample['context']}. Generate the SQL query for the question: {sample['question']} [/INST] {sample['answer']}</s>"""

def load_and_prepare_dataset(dataset_name, tokenizer, split="train"):
    """
    Loads a dataset, formats it, and tokenizes it for SFT.

    Args:
        dataset_name (str): The name of the dataset on Hugging Face Hub.
        tokenizer: The tokenizer to use for encoding the text.
        split (str): The dataset split to load (e.g., "train", "test").

    Returns:
        The processed and tokenized dataset.
    """
    # Load the dataset
    dataset = load_dataset(dataset_name, split=split)

    # Apply the formatting and tokenization
    # The map function is highly efficient for processing datasets.
    tokenized_dataset = dataset.map(
        lambda sample: tokenizer(format_prompt(sample)),
        batched=True,
        remove_columns=list(dataset.features) # Remove original columns to keep only tokenized inputs
    )
    
    return tokenized_dataset
