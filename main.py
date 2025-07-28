import argparse
from sudo_sql.inference.engine import get_engine

def main():
    parser = argparse.ArgumentParser(description="sudo-SQL: Text-to-SQL Generation")
    parser.add_argument("question", type=str, help="The natural language question to translate to SQL.")
    parser.add_argument("schema_path", type=str, help="Path to the file containing the database schema.")
    parser.add_argument("--provider", action="append", required=True,
                        help="Specify a provider from configs/models.yaml. Can be used multiple times.")
    parser.add_argument("--config", type=str, default="configs/models.yaml",
                        help="Path to the configuration file.")
    
    # Mutually exclusive group for run mode
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--use-critic", action="store_true", help="Use the Critic Agent to review the primary model's SQL.")
    mode_group.add_argument("--voting", action="store_true", help="Use multi-model voting to determine the best SQL.")

    args = parser.parse_args()

    # Read the schema from the file
    with open(args.schema_path, 'r') as f:
        schema = f.read()

    # Get the inference engine
    engine = get_engine(provider_names=args.provider, config_path=args.config, with_critic=args.use_critic)

    # Generate the SQL query based on the selected mode
    if args.voting:
        print(f"Running with multi-model voting across {len(args.provider)} providers...")
        sql_query = engine.run_with_voting(question=args.question, schema=schema)
    elif args.use_critic:
        print(f"Running with Critic Agent on primary provider: {args.provider[0]}...")
        sql_query = engine.run_with_critic(question=args.question, schema=schema)
    else:
        print(f"Running with primary provider: {args.provider[0]}...")
        sql_query = engine.run(question=args.question, schema=schema)

    print("\nFinal SQL Query:")
    print(sql_query)

if __name__ == "__main__":
    main()
