from .base import BaseDataLoader
from .spider import SpiderLoader
from .bird import BirdLoader

def get_data_loader(dataset_name: str, data_path: str) -> BaseDataLoader:
    if dataset_name.lower() == "spider":
        return SpiderLoader(data_path)
    elif dataset_name.lower() == "bird":
        return BirdLoader(data_path)
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
