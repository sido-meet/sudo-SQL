import sqlite3
from typing import Tuple
from sudo_sql.environments.base import BaseEnvironment

class SQLExecutionEnvironment(BaseEnvironment):
    """
    An environment that executes a SQL query against a database and provides a reward.
    """
    def __init__(self, db_path: str):
        """
        Initializes the environment.

        Args:
            db_path: The path to the SQLite database file.
        """
        self.db_path = db_path

    def step(self, generated_sql: str) -> Tuple[str, float]:
        """
        Executes the SQL query and returns a reward.

        Args:
            generated_sql: The SQL query to execute.

        Returns:
            A tuple containing the observation (result or error) and the reward.
        """
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute(generated_sql)
            result = cursor.fetchall()
            reward = 1.0
            observation = str(result)
        except Exception as e:
            reward = -1.0
            observation = str(e)
        finally:
            if 'con' in locals():
                con.close()
        
        return observation, reward
