import pytest
import yaml
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

import sys
sys.path.insert(0, ".")

from main import app


@pytest.fixture
def mock_openai():
    with patch('sudo_sql.pipeline.OpenAIProvider') as mock_provider:
        mock_instance = mock_provider.return_value
        mock_instance.generate.return_value = "SELECT * FROM mocked_users;"
        yield mock_provider


def test_infer_command(mock_openai):
    """Test the inference command with a mocked OpenAI provider."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["infer", "--config", "configs/infer.yaml"],
    )

    assert result.exit_code == 0
    assert "SELECT * FROM mocked_users;" in result.stdout

    # Verify that the provider was called with the correct prompt
    with open("configs/infer.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    infer_config = config['inference']
    question = infer_config['question']
    schema = infer_config['schema']
    expected_prompt = f"Given the schema: {schema}, generate the SQL for: {question}"

    mock_openai.return_value.generate.assert_called_once_with(expected_prompt)