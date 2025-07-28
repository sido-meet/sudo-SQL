import argparse
from sudo_sql.inference.engine import get_engine

def main():
    parser = argparse.ArgumentParser(description="sudo-SQL: Text-to-SQL Generation")
    parser.add_argument("question", type=str, help="The natural language question to translate to SQL.")
    parser.add_argument("schema_path", type=str, help="Path to the file containing the database schema.")
    parser.add_argument("--provider", type=str, default="openai", choices=["openai", "huggingface"],
                        help="The model provider to use.")
    parser.add_argument("--config", type=str, default="configs/models.yaml",
                        help="Path to the configuration file.")
    parser.add_argument("--use-critic", action="store_true", help="Use the Critic Agent to review and correct the SQL.")
    
    args = parser.parse_args()

    # Read the schema from the file
    with open(args.schema_path, 'r') as f:
        schema = f.read()

    # Get the inference engine
    engine = get_engine(provider_name=args.provider, config_path=args.config, with_critic=args.use_critic)

    # Generate the SQL query
    if args.use_critic:
        print("Running with Critic Agent...")
        sql_query = engine.run_with_critic(question=args.question, schema=schema)
    else:
        sql_query = engine.run(question=args.question, schema=schema)

    print("\nFinal SQL Query:")
    print(sql_query)

if __name__ == "__main__":
    main()
