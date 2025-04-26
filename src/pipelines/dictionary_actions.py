from pathlib import Path

import pandas as pd

from src.database.connection import get_session
from src.database.repositories.language_repository import LanguageRepository
from src.database.repositories.dictionary_repository import DictionaryRepository
from src.helpers.validators import DataframeValidators
from src.parsers.xml_parser import XmlParser


class DictionaryImportPipeline(DataframeValidators):
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.progress_row = None
        self.progress_value = None

    def run(self):
        df = self.read_file(self.file_path)
        self.validate_dataframe(df=df)
        self.add_in_database(df=df)

    @classmethod
    def read_file(cls, file_path: Path):
        if file_path.suffix == '.csv':
            return pd.read_csv(file_path, encoding='utf-8', sep=',')
        if file_path.suffix == '.xlsx':
            return pd.read_excel(file_path, engine='openpyxl')
        
    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> bool:
        cls.validate_columns(df=df)
        cls.validate_languages(df=df)
        cls.validate_nulls(df=df, ignore_columns=['uid'])
        return True
    
    @classmethod
    def add_in_database(cls, df: pd.DataFrame) -> bool:
        with get_session() as session:
            for idx, row in df.iterrows():
                DictionaryRepository.upsert_translation(
                    session=session, 
                    source_language=row['source_language'], 
                    target_language=row['target_language'], 
                    source_text=row['source_text'], 
                    target_text=row['target_text'], 
                    mod_name=row['mod_name'], 
                    uid=row['uid'],
                )


class DictionaryExportPipeline:
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.progress_value = None

    def run(self):
        self.get_export_data()
        self.export()

    def get_export_data(self) -> pd.DataFrame:
        with get_session() as session:
            translations = DictionaryRepository.get_all_data(session=session)
            self.df = pd.DataFrame(translations)

    def export(self):
        if self.file_path.suffix == '.csv':
            self.df.to_csv(self.file_path, index=False)
        elif self.file_path.suffix == '.xlsx':
            self.df.to_excel(self.file_path, index=False)
        else:
            raise ValueError('File format not supported. Please use .csv or .xlsx')


class DictionaryCreationPipeline:
    def __init__(self, source_path: Path, target_path: Path, source_language: str, target_language, mod_name: str):
        self.source_path = Path(source_path)
        self.target_path = Path(target_path)
        self.source_language = source_language
        self.target_language = target_language
        self.mod_name = mod_name
        self.progress_value = None

    def run(self):
        self.read_file()
        self.get_languages_code()
        self.create_data()
        self.upsert_data()

    def read_file(self):
        df_source = XmlParser.xml_to_dataframe(xml_path=self.source_path)
        df_source.rename(columns={'text': 'source_text'}, inplace=True)
        df_target = XmlParser.xml_to_dataframe(xml_path=self.target_path)
        df_target.rename(columns={'text': 'target_text'}, inplace=True)
        self.merged = pd.merge(df_source, df_target, on='contentuid', how='outer')
        self.merged = self.merged.dropna()

    def get_languages_code(self):
        with get_session() as session:
            self.source_language_code = LanguageRepository.find_language_by_name(session=session, name=self.source_language)
            self.target_language_code = LanguageRepository.find_language_by_name(session=session, name=self.target_language)

    def create_data(self):
        self.merged['source_language'] = self.source_language_code
        self.merged['target_language'] = self.target_language_code
        self.merged['mod_name'] = self.mod_name
        self.merged['uid'] = self.merged['contentuid']
        self.merged = self.merged[['source_language', 'target_language', 'source_text', 'target_text', 'mod_name', 'uid']]

    def upsert_data(self):
        with get_session() as session:
            for idx, row in self.merged.iterrows():
                DictionaryRepository.upsert_translation(
                    session=session, 
                    source_language=row['source_language'], 
                    target_language=row['target_language'], 
                    source_text=row['source_text'], 
                    target_text=row['target_text'], 
                    mod_name=row['mod_name'], 
                    uid=row['uid'],
                )
