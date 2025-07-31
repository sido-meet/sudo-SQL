import pytest
import yaml
import json
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
import sys
import os

sys.path.insert(0, ".")
from main import app

# --- Test Data ---
MOCK_DATASET = [
    {
        'question': 'Question 1: What is the capital of France?',
        'sql': 'SELECT capital FROM countries WHERE name = "France"',
        'db_id': 'countries',
        'db_path': '/tmp/countries.sqlite',
        'schema': 'CREATE TABLE countries (name TEXT, capital TEXT)',
        'evidence': None,
        'difficulty': None
    },
    {
        'question': 'Question 2: How many continents are there?',
        'sql': 'SELECT count(*) FROM continents',
        'db_id': 'continents',
        'db_path': '/tmp/continents.sqlite',
        'schema': 'CREATE TABLE continents (name TEXT)',
        'evidence': None,
        'difficulty': None
    }
]

# --- Fixtures ---

@pytest.fixture
def mock_logger():
    with patch('sudo_sql.pipeline.logger') as mock_log:
        yield mock_log

@pytest.fixture
def mock_openai_provider():
    with patch('sudo_sql.pipeline.OpenAIProvider') as mock_provider_cls:
        mock_provider_instance = mock_provider_cls.return_value
        mock_provider_instance.generate.return_value = "mocked_sql_result"
        yield mock_provider_instance

@pytest.fixture
def mock_data_loader():
    with patch('sudo_sql.pipeline.get_data_loader') as mock_get_loader:
        mock_loader_instance = MagicMock()
        mock_loader_instance.load_data.return_value = MOCK_DATASET
        mock_get_loader.return_value = mock_loader_instance
        yield mock_get_loader

@pytest.fixture
def create_config(tmp_path):
    def _create_config(save_mode):
        config_path = tmp_path / "test_config.yaml"
        config_data = {
            'mode': 'infer',
            'model': {'provider': 'openai', 'name': 'TestModel'},
            'inference': {
                'dataset_name': 'test_ds',
                'data_path': '/fake/path',
                'split': 'dev',
                'schema_type': 'ddl-schema',
                'use_cache': False,
                'output': {
                    'save_path': str(tmp_path),
                    'save_mode': save_mode
                }
            }
        }
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f)
        return str(config_path)
    return _create_config

# --- Tests ---

def test_resume_mode_with_existing_file(create_config, tmp_path, mock_data_loader, mock_openai_provider, mock_logger):
    """Tests that 'resume' mode correctly skips processed items."""
    # Setup: Create a pre-existing results file with the first question already processed
    results_file = tmp_path / "test_ds_dev_TestModel.jsonl"
    pre_existing_result = {
        "db_id": "countries",
        "question": "Question 1: What is the capital of France?",
        "generated_sql": "old_sql_result",
        "ground_truth_sql": "SELECT capital FROM countries WHERE name = \"France\""
    }
    with open(results_file, 'w') as f:
        f.write(json.dumps(pre_existing_result) + '\n')

    config_file = create_config(save_mode="resume")
    runner = CliRunner()
    result = runner.invoke(app, ["infer", "--config", config_file])

    assert result.exit_code == 0
    mock_logger.info.assert_any_call(f"Resuming inference run. Loading previously generated results from {results_file}...")
    mock_logger.info.assert_any_call("Found 1 previously completed items. Skipping...")
    
    # Assert that generate was only called for the *second* question
    mock_openai_provider.generate.assert_called_once()
    call_args = mock_openai_provider.generate.call_args[0][0]
    assert "Question 2" in call_args

    # Assert that the final file has both results
    with open(results_file, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2
    assert "old_sql_result" in lines[0]
    assert "mocked_sql_result" in lines[1]

@patch('sudo_sql.pipeline.datetime')
def test_overwrite_mode(mock_datetime, create_config, tmp_path, mock_data_loader, mock_openai_provider):
    """Tests that 'overwrite' mode creates a new, timestamped file."""
    mock_datetime.now.return_value.strftime.return_value = "mock_timestamp"
    config_file = create_config(save_mode="overwrite")
    runner = CliRunner()
    result = runner.invoke(app, ["infer", "--config", config_file])

    assert result.exit_code == 0
    assert mock_openai_provider.generate.call_count == 2
    
    # Assert that the file has the timestamp and was created
    expected_file = tmp_path / "test_ds_dev_TestModel_mock_timestamp.jsonl"
    assert expected_file.exists()
    with open(expected_file, 'r') as f:
        assert len(f.readlines()) == 2

def test_resume_mode_with_no_file(create_config, tmp_path, mock_data_loader, mock_openai_provider):
    """Tests that 'resume' mode with no existing file works correctly."""
    config_file = create_config(save_mode="resume")
    runner = CliRunner()
    result = runner.invoke(app, ["infer", "--config", config_file])

    assert result.exit_code == 0
    assert mock_openai_provider.generate.call_count == 2

    # Assert that the file has the deterministic name
    expected_file = tmp_path / "test_ds_dev_TestModel.jsonl"
    assert expected_file.exists()
    with open(expected_file, 'r') as f:
        assert len(f.readlines()) == 2