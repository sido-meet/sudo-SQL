import pytest
import yaml
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

import sys
sys.path.insert(0, ".")

from main import app

@pytest.fixture
def mock_logger():
    with patch('sudo_sql.pipeline.logger') as mock_log:
        yield mock_log

@pytest.fixture
def mock_data_loader():
    with patch('sudo_sql.pipeline.get_data_loader') as mock_get_loader:
        mock_loader_instance = MagicMock()
        mock_loader_instance.load_data.return_value = [
            {
                'question': 'What is the capital of France?',
                'sql': 'SELECT capital FROM countries WHERE name = "France"',
                'db_id': 'countries',
                'db_path': '/tmp/countries.sqlite',
                'schema': 'CREATE TABLE countries (name TEXT, capital TEXT)',
                'evidence': None,
                'difficulty': None
            }
        ]
        mock_get_loader.return_value = mock_loader_instance
        yield mock_get_loader

@patch('sudo_sql.pipeline.OpenAIProvider')
def test_infer_command_with_mocked_loader(mock_openai_provider, mock_data_loader, mock_logger):
    """Test the inference command with a mocked data loader and OpenAI provider."""
    mock_openai_instance = mock_openai_provider.return_value
    mock_openai_instance.generate.return_value = "SELECT capital FROM countries WHERE name = 'France'"

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["infer", "--config", "configs/infer.yaml"],
    )

    assert result.exit_code == 0

    # Verify that the logger was called correctly
    mock_logger.info.assert_any_call("--- Running Inference ---")
    mock_logger.info.assert_any_call("Using OpenAI provider with model: Qwen2.5-3B-Instruct")
    mock_logger.debug.assert_called_once_with("Generating SQL for question: What is the capital of France?")
    mock_logger.info.assert_any_call("--- Inference complete ---")

    # Verify that the data loader was called correctly
    mock_data_loader.return_value.load_data.assert_called_once_with("dev", "ddl-schema", True)

    # Verify that the OpenAI provider was called with the correct prompt
    expected_prompt = "Given the schema: CREATE TABLE countries (name TEXT, capital TEXT), generate the SQL for: What is the capital of France?"
    mock_openai_instance.generate.assert_called_once_with(expected_prompt)
