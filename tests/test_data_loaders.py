import pytest
from unittest.mock import patch, mock_open
import os

from sudo_sql.data_loaders import get_data_loader, SpiderLoader, BirdLoader

def test_get_data_loader_spider():
    loader = get_data_loader("spider", "./data/spider")
    assert isinstance(loader, SpiderLoader)

def test_get_data_loader_bird():
    loader = get_data_loader("bird", "./data/BIRD")
    assert isinstance(loader, BirdLoader)

def test_get_data_loader_unknown():
    with pytest.raises(ValueError):
        get_data_loader("unknown_dataset", "./data")

@patch("sudo_sql.data_loaders.spider.open", new_callable=mock_open, read_data='[{"db_id": "test_db", "question": "test question", "query": "SELECT * FROM test"}]')
@patch("sudo_sql.data_loaders.base.BaseDataLoader._get_schema", return_value="CREATE TABLE test (id INT)")
def test_spider_loader(mock_get_schema, mock_file):
    loader = SpiderLoader("./data/spider")
    data = loader.load_data("dev")
    assert len(data) == 1
    assert data[0]["question"] == "test question"
    assert data[0]["sql"] == "SELECT * FROM test"
    assert data[0]["db_id"] == "test_db"
    assert data[0]["schema"] == "CREATE TABLE test (id INT)"

@patch("sudo_sql.data_loaders.bird.os.listdir", return_value=["dev_20240627"])
@patch("sudo_sql.data_loaders.bird.open", new_callable=mock_open, read_data='[{"db_id": "bird_db", "question": "bird question", "SQL": "SELECT name FROM birds", "evidence": "bird evidence", "difficulty": "easy"}]')
@patch("sudo_sql.data_loaders.base.BaseDataLoader._get_schema", return_value="CREATE TABLE birds (name TEXT)")
def test_bird_loader(mock_get_schema, mock_file, mock_listdir):
    loader = BirdLoader("./data/BIRD")
    data = loader.load_data("dev")
    assert len(data) == 1
    assert data[0]["question"] == "bird question"
    assert data[0]["sql"] == "SELECT name FROM birds"
    assert data[0]["db_id"] == "bird_db"
    assert data[0]["schema"] == "CREATE TABLE birds (name TEXT)"
    assert data[0]["evidence"] == "bird evidence"
    assert data[0]["difficulty"] == "easy"
