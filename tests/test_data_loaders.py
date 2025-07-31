import pytest
import os
import time
from unittest.mock import patch, MagicMock

from sudo_sql.data_loaders.base import BaseDataLoader

# A concrete implementation for testing the abstract BaseDataLoader's methods
class ConcreteLoader(BaseDataLoader):
    def load_data(self, split: str, schema_type: str, use_cache: bool) -> list:
        return []

@pytest.fixture
def loader(tmp_path):
    """Provides a concrete loader instance and a temporary data path."""
    return ConcreteLoader(data_path=str(tmp_path))

@pytest.fixture
def mock_d_schema():
    """Mocks the d-schema components."""
    with patch('sudo_sql.data_loaders.base.DatabaseParser') as mock_parser_cls:
        with patch('sudo_sql.data_loaders.base.DDLSchemaGenerator') as mock_generator_cls:
            mock_parser_instance = MagicMock()
            mock_parser_cls.return_value = mock_parser_instance
            mock_parser_instance.parse.return_value = "parsed_schema"

            mock_generator_instance = MagicMock()
            mock_generator_cls.return_value = mock_generator_instance
            mock_generator_instance.generate_schema.return_value = "generated_ddl_schema"
            
            yield mock_parser_cls, mock_generator_cls

@patch('os.getcwd')
def test_cache_miss(mock_getcwd, loader, tmp_path, mock_d_schema):
    """Test that d-schema is called and a cache file is created when no cache exists."""
    mock_getcwd.return_value = str(tmp_path)
    db_path = tmp_path / "test.db"
    db_path.touch()

    schema = loader._get_schema(str(db_path), "ddl-schema", True, "test_ds", "test_db")

    assert schema == "generated_ddl_schema"
    mock_d_schema[0].assert_called_once()
    mock_d_schema[1].assert_called_once()

    cache_path = tmp_path / "cache/schemas/test_ds/test_db/ddl-schema.txt"
    assert cache_path.exists()
    assert cache_path.read_text() == "generated_ddl_schema"

@patch('os.getcwd')
def test_cache_hit(mock_getcwd, loader, tmp_path, mock_d_schema):
    """Test that the cached schema is used and d-schema is not called when cache is valid."""
    mock_getcwd.return_value = str(tmp_path)
    db_path = tmp_path / "test.db"
    db_path.touch()

    cache_dir = tmp_path / "cache/schemas/test_ds/test_db"
    cache_dir.mkdir(parents=True)
    cache_path = cache_dir / "ddl-schema.txt"
    cache_path.write_text("cached_schema")
    time.sleep(0.1)
    db_path.touch() # Make sure db is older
    time.sleep(0.1)
    cache_path.touch() # Make sure cache is newer

    schema = loader._get_schema(str(db_path), "ddl-schema", True, "test_ds", "test_db")

    assert schema == "cached_schema"
    mock_d_schema[0].assert_not_called()
    mock_d_schema[1].assert_not_called()

@patch('os.getcwd')
def test_stale_cache(mock_getcwd, loader, tmp_path, mock_d_schema):
    """Test that d-schema is called and cache is updated when cache is stale."""
    mock_getcwd.return_value = str(tmp_path)
    cache_dir = tmp_path / "cache/schemas/test_ds/test_db"
    cache_dir.mkdir(parents=True)
    cache_path = cache_dir / "ddl-schema.txt"
    cache_path.write_text("stale_schema")

    time.sleep(0.1)

    db_path = tmp_path / "test.db"
    db_path.touch()

    schema = loader._get_schema(str(db_path), "ddl-schema", True, "test_ds", "test_db")

    assert schema == "generated_ddl_schema"
    mock_d_schema[0].assert_called_once()
    mock_d_schema[1].assert_called_once()
    assert cache_path.read_text() == "generated_ddl_schema"

@patch('os.getcwd')
def test_cache_disabled(mock_getcwd, loader, tmp_path, mock_d_schema):
    """Test that d-schema is called even if a valid cache exists when use_cache=False."""
    mock_getcwd.return_value = str(tmp_path)
    db_path = tmp_path / "test.db"
    db_path.touch()

    cache_dir = tmp_path / "cache/schemas/test_ds/test_db"
    cache_dir.mkdir(parents=True)
    cache_path = cache_dir / "ddl-schema.txt"
    cache_path.write_text("cached_schema")

    schema = loader._get_schema(str(db_path), "ddl-schema", False, "test_ds", "test_db")

    assert schema == "generated_ddl_schema"
    mock_d_schema[0].assert_called_once()
