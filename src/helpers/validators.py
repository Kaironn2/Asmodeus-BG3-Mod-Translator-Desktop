import pandas as pd

from src.database.connection import get_session
from src.database.repositories.language_repository import LanguageRepository


class Validators:

    @staticmethod
    def validate_mod_name(mod_name: str) -> str:
        if not mod_name or not isinstance(mod_name, str):
            raise ValueError('O nome de mod não pode ser vazio ou nulo.')
        
        to_replace = [
            ('_', ''),
            (' - ', '_'),
            (' ', '_'),
            ('-', '_'),
            ('/', '_'),
            ('\\', '_'),
            (':', '_'),
            ('*', '_'),
            ('?', '_'),
            ('"', '_'),
            ('<', '_'),
            ('>', '_'),
            ('|', '_')
        ]
        for old, new in to_replace:
            mod_name = mod_name.replace(old, new)
        return mod_name.lower()
    

class DataframeValidators:
    required_columns = ['source_language', 'target_language', 'source_text', 'target_text', 'mod_name', 'uid']

    @classmethod
    def validate_columns(cls, df: pd.DataFrame) -> bool:
        for col in cls.required_columns:
            if col not in df.columns:
                raise ValueError(f'Missing required column: {col}')
        return True
    
    @classmethod
    def validate_languages(cls, df: pd.DataFrame) -> bool:
        with get_session() as session:
            valid_languages = set(LanguageRepository.get_all_language_codes(session=session))
            invalid_languages = set(df['source_language'].unique()).union(set(df['target_language'].unique())) - valid_languages
            if invalid_languages:
                raise ValueError(f'Invalid languages found: {', '.join(invalid_languages)}')
        return True
    
    @classmethod
    def validate_nulls(cls, df: pd.DataFrame, ignore_columns: list = None) -> bool:
        cols_to_check = [col for col in df.columns if col not in ignore_columns]
        if df[cols_to_check].isnull().values.any():
            raise ValueError('File contains null values')
        return True
