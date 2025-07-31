import os
import json
from .base import BaseDataLoader, StandardizedDataFormat

class BirdLoader(BaseDataLoader):
    def load_data(self, split: str) -> list[StandardizedDataFormat]:
        # BIRD has a nested structure, so we need to find the correct subdirectory
        # For simplicity, we'll assume the first subdirectory found is the correct one.
        # A more robust solution might involve configuration.
        split_dir = ""
        for d in os.listdir(self.data_path):
            if d.startswith(split):
                split_dir = os.path.join(self.data_path, d)
                break
        
        if not split_dir:
            raise FileNotFoundError(f"Could not find data directory for split: {split}")

        json_path = os.path.join(split_dir, f'{split}.json')
        with open(json_path, 'r') as f:
            data = json.load(f)

        processed_data = []
        for item in data:
            db_id = item['db_id']
            db_path = os.path.join(split_dir, 'dev_databases', db_id, f'{db_id}.sqlite')
            schema = self._get_schema(db_path)

            processed_data.append({
                'question': item['question'],
                'sql': item['SQL'],
                'db_id': db_id,
                'db_path': db_path,
                'schema': schema,
                'evidence': item.get('evidence'),
                'difficulty': item.get('difficulty')
            })
        return processed_data
