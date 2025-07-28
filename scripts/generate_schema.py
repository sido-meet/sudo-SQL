# scripts/generate_schema.py

import argparse
from d_schema.generator import SchemaGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate a database schema using D-Schema.")
    
    parser.add_argument("--db_uri", type=str, required=True, 
                        help="Database connection URI (e.g., 'postgresql://user:pass@host/db').")
    parser.add_argument("--output_path", type=str, default="schema.sql",
                        help="Path to save the generated schema file.")
    parser.add_argument("--schema-type", type=str, default="ddl", 
                        choices=["ddl", "m-schema", "mac-sql"],
                        help="The type of schema representation to generate.")
    
    args = parser.parse_args()

    print(f"Connecting to {args.db_uri} to generate '{args.schema_type}' schema...")

    try:
        generator = SchemaGenerator(db_uri=args.db_uri)
        
        # Call the appropriate generation method based on the selected type
        if args.schema_type == "ddl":
            schema = generator.generate_ddl()
        elif args.schema_type == "m-schema":
            schema = generator.generate_m_schema()
        elif args.schema_type == "mac-sql":
            schema = generator.generate_mac_sql()
        else:
            # This case should not be reached due to 'choices' in argparse
            raise ValueError(f"Unknown schema type: {args.schema_type}")
            
        with open(args.output_path, 'w') as f:
            f.write(schema)
            
        print(f"Schema successfully generated and saved to {args.output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
