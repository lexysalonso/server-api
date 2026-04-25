import yaml
import os
from pathlib import Path
from typing import Any, Dict

_config: Dict[str, Any] = {}


def load_config() -> Dict[str, Any]:
    global _config
    if _config:
        return _config
    
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            _config = yaml.safe_load(f)
    else:
        _config = {}
    
    # Allow environment variables to override config
    if os.getenv("MONGO_URI"):
        _config.setdefault("database", {})["mongo_uri"] = os.getenv("MONGO_URI")
    if os.getenv("DB_NAME"):
        _config.setdefault("database", {})["db_name"] = os.getenv("DB_NAME")
    if os.getenv("INNOVASOFT_URL"):
        _config.setdefault("innovasoft", {})["base_url"] = os.getenv("INNOVASOFT_URL")
    
    return _config


def get_config() -> Dict[str, Any]:
    return load_config()


def get_mongo_uri() -> str:
    config = get_config()
    return config.get("database", {}).get("mongo_uri", "mongodb://localhost:27017")


def get_db_name() -> str:
    config = get_config()
    return config.get("database", {}).get("db_name", "innovasoft_api")


def get_innovasoft_url() -> str:
    config = get_config()
    return config.get("innovasoft", {}).get("base_url", "https://pruebareactjs.test-class.com/Api")


def get_innovasoft_timeout() -> int:
    config = get_config()
    return config.get("innovasoft", {}).get("timeout", 30)


def get_app_config() -> Dict[str, Any]:
    config = get_config()
    return config.get("app", {})