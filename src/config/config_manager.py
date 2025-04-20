import os
import json

from src.config.paths import JSON_CONFIG


class ConfigManager:

    @staticmethod
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
    
    @staticmethod
    def load_openai_key() -> str:
        if os.path.exists(JSON_CONFIG):
            with open(JSON_CONFIG, 'r', encoding='utf-8') as f:
                try:
                    config = json.load(f)
                    return config.get('openai_key', '')
                except Exception:
                    return ''
        return ''

    @staticmethod
    def save_last_languages(source_lang: str, target_lang: str):
        config = {}
        os.makedirs(os.path.dirname(JSON_CONFIG), exist_ok=True)
        if os.path.exists(JSON_CONFIG):
            with open(JSON_CONFIG, 'r', encoding='utf-8') as f:
                try:
                    config = json.load(f)
                except Exception:
                    config = {}
        config['last_source_lang'] = source_lang
        config['last_target_lang'] = target_lang
        with open(JSON_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_last_languages():
        if os.path.exists(JSON_CONFIG):
            with open(JSON_CONFIG, 'r', encoding='utf-8') as f:
                try:
                    config = json.load(f)
                    return (
                        config.get('last_source_lang', ''),
                        config.get('last_target_lang', '')
                    )
                except Exception:
                    return ('', '')
        return ('', '')
