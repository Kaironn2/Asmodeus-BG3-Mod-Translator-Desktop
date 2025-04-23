from pathlib import Path

from sqlmodel import Session

from src.database.connection import get_session
from src.database.repositories.dictionary_repository import DictionaryRepository
from src.database.repositories.language_repository import LanguageRepository
from src.parsers.xml_parser import XmlParser


class ManualTranslationPipeline:

    def __init__(self, xml_path: Path, mod_name:str, source_language: str, target_language: str):
        self.xml_path = xml_path
        self.mod_name = mod_name
        self.source_language = source_language
        self.target_language = target_language

    
    def run(self, session: Session) -> None:
        self._get_language_codes(session)
        self._sort_languages()
        self._get_dataframe()
        self._search_in_dictionary(session)
        return self.df


    def _get_language_codes(self, session: Session) -> None:
        self.source_language_code = LanguageRepository.find_language_by_name(
            session=session,
            name=self.source_language,
        )
        self.target_language_code = LanguageRepository.find_language_by_name(
            session=session,
            name=self.target_language,
        )

    
    def _sort_languages(self):
        db_lang1, db_lang2 = sorted([self.source_language_code, self.target_language_code])
        self.db_lang_code1 = db_lang1
        self.db_lang_code2 = db_lang2

        if self.source_language_code == db_lang1:
            self.source_db_col = 'text_language1'
            self.target_db_col = 'text_language2'
        else:
            self.source_db_col = 'text_language2'
            self.target_db_col = 'text_language1'


    def _get_dataframe(self) -> None:
        self.df = XmlParser.xml_to_dataframe(self.xml_path)
        self.df = self.df.rename(columns={'text': 'source_text'})
        self.df['text'] = ''

    
    def _search_in_dictionary(self, session: Session) -> None:
        for index, row in self.df.iterrows():
            source_text = row['source_text']
            content_uid = row['contentuid']
            
            result = DictionaryRepository.find_translations_by_uid(
                session=session,
                uid=content_uid,
                source_language=self.source_language_code,
                target_language=self.target_language_code,
            )

            if result is None:
                result = DictionaryRepository.find_translations_by_mod(
                    session=session,
                    mod_name=self.mod_name,
                    source_language=self.source_language_code,
                    target_language=self.target_language_code,
                    source_text=source_text,
                )

            if result is None:
                result = DictionaryRepository.find_translations_by_text(
                    session=session,
                    source_language=self.source_language_code,
                    target_language=self.target_language_code,
                    source_text=source_text,
                )

            if result is not None:
                if hasattr(result, self.target_db_col):
                    self.df.at[index, 'text'] = getattr(result, self.target_db_col)
                elif isinstance(result, str):
                    self.df.at[index, 'text'] = result
