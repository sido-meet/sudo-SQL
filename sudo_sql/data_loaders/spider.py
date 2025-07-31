import os
import json
from .base import BaseDataLoader, StandardizedDataFormat

class SpiderLoader(BaseDataLoader):
    def load_data(self, split: str) -> list[StandardizedDataFormat]:
        if split == 'train':
            json_path = os.path.join(self.data_path, 'train_spider.json')
        else:
            json_path = os.path.join(self.data_path, f'{split}.json')

        with open(json_path, 'r') as f:
            data = json.load(f)

        processed_data = []
        for item in data:
            db_id = item['db_id']
            db_path = os.path.join(self.data_path, 'database', db_id, f'{db_id}.sqlite')
            schema = self._get_schema(db_path)

            processed_data.append({
                'question': item['question'],
                'sql': item['query'],
                'db_id': db_id,
                'db_path': db_path,
                'schema': schema,
                'evidence': None,
                'difficulty': None
            })
        return processed_data
