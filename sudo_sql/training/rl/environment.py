# sudo_sql/training/rl/environment.py

import sqlite3
from typing import Tuple

class SQLExecutionEnvironment:
    """
    A simple environment that executes an SQL query against a database
    and provides a reward based on the outcome.
    """
    def __init__(self, db_path: str):
        """
        Initializes the environment.

        Args:
            db_path: The path to the SQLite database file.
        """
        self.db_path = db_path

    def step(self, sql_query: str) -> Tuple[bool, float]:
        """
        Executes the SQL query and returns a reward.

        Args:
            sql_query: The SQL query to execute.

        Returns:
            A tuple containing:
            - done (bool): Always True in this simple case, as each step is one episode.
            - reward (float): The reward for the action.
        """
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute(sql_query)
            cursor.fetchall()
            # Positive reward for successful execution
            reward = 1.0
        except Exception:
            # Negative reward for any execution error
            reward = -1.0
        finally:
            if 'con' in locals():
                con.close()
        
        return True, reward
