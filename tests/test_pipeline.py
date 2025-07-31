import pytest
import yaml
from unittest.mock import patch

from sudo_sql.pipeline import get_pipeline
from sudo_sql.pipeline.inference import InferencePipeline
from sudo_sql.pipeline.sft import SFTPipeline
from sudo_sql.pipeline.rl import RLPipeline

@pytest.fixture
def mock_config(tmp_path):
    def _create_config(mode):
        config_path = tmp_path / f"{mode}_config.yaml"
        config_data = {'mode': mode, 'model': {}}
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f)
        return str(config_path)
    return _create_config

def test_get_pipeline_inference(mock_config):
    config_path = mock_config("infer")
    pipeline = get_pipeline(config_path)
    assert isinstance(pipeline, InferencePipeline)

def test_get_pipeline_sft(mock_config):
    config_path = mock_config("sft")
    pipeline = get_pipeline(config_path)
    assert isinstance(pipeline, SFTPipeline)

def test_get_pipeline_rl(mock_config):
    config_path = mock_config("rl")
    pipeline = get_pipeline(config_path)
    assert isinstance(pipeline, RLPipeline)

def test_get_pipeline_unknown(mock_config):
    config_path = mock_config("unknown")
    with pytest.raises(ValueError):
        get_pipeline(config_path)
