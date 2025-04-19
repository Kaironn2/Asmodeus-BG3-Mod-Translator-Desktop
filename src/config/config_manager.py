import os
import json

from src.config.paths import JSON_CONFIG

def save_openai_key(key: str):
    config = {}
    os.makedirs(os.path.dirname(JSON_CONFIG), exist_ok=True)
    if os.path.exists(JSON_CONFIG):
        with open(JSON_CONFIG, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
            except Exception:
                config = {}
    config['openai_key'] = key
    with open(JSON_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_openai_key() -> str:
    if os.path.exists(JSON_CONFIG):
        with open(JSON_CONFIG, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                return config.get('openai_key', '')
            except Exception:
                return ''
    return ''
