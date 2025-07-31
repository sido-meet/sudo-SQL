from abc import ABC, abstractmethod
from typing import TypedDict, Optional
import sqlite3

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
    def load_data(self, split: str) -> list[StandardizedDataFormat]:
        """Loads data for a given split (e.g., 'train', 'dev')."""
        pass

    def _get_schema(self, db_path: str) -> str:
        """
        Extracts the CREATE TABLE statements from a SQLite database.
        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            schema = ""
            for table in tables:
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table[0]}';")
                schema += cursor.fetchone()[0] + "\n"
        return schema
