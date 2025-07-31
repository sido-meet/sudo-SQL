# scripts/generate_schema.py

import argparse
from d_schema import (
    DatabaseParser,
    DDLSchemaGenerator,
    MSchemaGenerator,
    MacSQLSchemaGenerator
)

# Map schema type keys to their corresponding generator classes
available_generators = {
    "ddl": DDLSchemaGenerator,
    "m-schema": MSchemaGenerator,
    "mac-sql": MacSQLSchemaGenerator,
}

def main():
    parser = argparse.ArgumentParser(description="Generate a database schema using D-Schema.")
    
    parser.add_argument("--db_url", type=str, required=True, 
                        help="Database connection URL (e.g., 'postgresql://user:pass@host/db').")
    parser.add_argument("--output_path", type=str, default="schema.sql",
                        help="Path to save the generated schema file.")
    parser.add_argument("--schema_type", type=str, default="ddl", 
                        choices=available_generators.keys(),
                        help="The type of schema representation to generate.")
    parser.add_argument("--profile", action="store_true",
                        help="Enable profiling to gather statistics about the database.")

    args = parser.parse_args()

    print(f"Generating '{args.schema_type}' schema for {args.db_url}...")

    try:
        # 1. Parse the database
        db_parser = DatabaseParser(db_url=args.db_url)
        database_schema = db_parser.parse(profile=args.profile)
        print("Database parsed successfully.")

        # 2. Get the selected generator class and instantiate it with the correct arguments
        print(f"Generating {args.schema_type} schema...")
        if args.schema_type == "m-schema":
            generator_instance = MSchemaGenerator(schema=database_schema)
        else:
            GeneratorClass = available_generators.get(args.schema_type)
            generator_instance = GeneratorClass(tables=database_schema.tables)

        # 3. Generate the schema string
        output_schema = generator_instance.generate_schema()

        # 4. Write the schema to the output file
        with open(args.output_path, 'w') as f:
            f.write(output_schema)
            
        print(f"Schema successfully generated and saved to {args.output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()