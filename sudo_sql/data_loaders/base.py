from abc import ABC, abstractmethod
from typing import TypedDict, Optional
import os
import sqlite3
from d_schema.db_parser import DatabaseParser
from d_schema.generators.ddl_schema.generator import DDLSchemaGenerator

class StandardizedDataFormat(TypedDict):
    question: str
    sql: str
    db_id: str
    db_path: str
    schema: str
    evidence: Optional[str]
    difficulty: Optional[str]

class BaseDataLoader(ABC):
    def __init__(self, data_path: str):
        self.data_path = data_path

    @abstractmethod
    def load_data(self, split: str, schema_type: str, use_cache: bool) -> list[StandardizedDataFormat]:
        pass

    def _generate_schema_with_d_schema(self, db_path: str, schema_type: str) -> str:
        db_url = f"sqlite:///{db_path}"
        db_parser = DatabaseParser(db_url=db_url)
        database_schema = db_parser.parse()

        # Simple factory for now
        if schema_type == "ddl-schema":
            generator = DDLSchemaGenerator(schema=database_schema)
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")

        return generator.generate_schema()

    def _get_schema(self, db_path: str, schema_type: str, use_cache: bool, dataset_name: str, db_id: str) -> str:
        if not use_cache:
            return self._generate_schema_with_d_schema(db_path, schema_type)

        cache_path = os.path.join(os.getcwd(), "cache", "schemas", dataset_name, db_id, f"{schema_type}.txt")

        if os.path.exists(cache_path):
            db_mod_time = os.path.getmtime(db_path)
            cache_mod_time = os.path.getmtime(cache_path)
            if cache_mod_time > db_mod_time:
                with open(cache_path, 'r') as f:
                    return f.read()

        new_schema = self._generate_schema_with_d_schema(db_path, schema_type)
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, 'w') as f:
            f.write(new_schema)
        return new_schema