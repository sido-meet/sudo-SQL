import yaml
from .base import BasePipeline
from .inference import InferencePipeline
from .sft import SFTPipeline
from .rl import RLPipeline

def get_pipeline(config_path: str) -> BasePipeline:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    mode = config.get("mode")
    if mode == "sft":
        return SFTPipeline(config)
    elif mode == "rl":
        return RLPipeline(config)
    elif mode == "infer":
        return InferencePipeline(config)
    else:
        raise ValueError(f"Unknown pipeline mode: {mode}")
