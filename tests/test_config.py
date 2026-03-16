import os
import yaml
import pytest

def test_config_loading():
    config_path = "config.yaml"
    assert os.path.exists(config_path)
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    assert "context" in config
    assert "guardrails" in config
    assert "llm" in config
    assert config["context_scanning"]["enabled"] is True
