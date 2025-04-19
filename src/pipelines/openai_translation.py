from pathlib import Path

import pandas as pd
from sqlmodel import Session

from src.config import paths
from src.helpers.validators import Validators
from src.parsers.lsx_parser import LsxParser
from src.parsers.xml_parser import XmlParser
from src.services.external_tools.lslib_service import LslibService
from src.services.openai.openai_service import OpenAIService
from src.services.openai.prompts import OpenAIPrompt
from src.database.repositories.dictionary_repository import DictionaryRepository
from src.database.repositories.language_repository import LanguageRepository


class OpenAITranslationPipeline:

    def __init__(
        self, session: Session, mod_name: str, mod_path: Path, source_language: str, target_language: str,
        author: str, description: str,
        ) -> None:
        
        self.session = session
        self.mod_name = Validators.validate_mod_name(mod_name) + f'_{target_language}'
        self.mod_path = mod_path
        self.source_language = source_language
        self.target_language = target_language
        self.author = author
        self.description = description

        self.target_language_name = LanguageRepository.find_language_by_code(
            session=self.session,
            code=self.target_language,
        )

        self.openai_prompt = OpenAIPrompt(
            source_lang=source_language,
            target_lang=target_language,
            session=session,
        )
        self.openai_service = OpenAIService()


    
    def run(self) -> None:
        self._mod_unpack()
        self._create_folder_structure()
        self._create_meta()
        self._translate()
        self._mod_pack()

    
    def _mod_unpack(self) -> None:
        self.xml_paths, self.meta_path = LslibService.mod_unpack(
            mod_path=self.mod_path,
            mod_name=self.mod_name,
            just_localization=True,
            session=self.session,
            source_language=self.source_language,
            target_language=self.target_language,
        )

    
    def _mod_pack(self) -> None:
        paths.PACKED.mkdir(exist_ok=True, parents=True)
        LslibService.mod_pack(
            input_folder=paths.TRANSLATED / self.mod_name,
            output_folder=paths.PACKED / Validators.validate_mod_name(self.mod_name),
        )

    
    def _create_folder_structure(self) -> None:
        self.mod_translated_path = paths.TRANSLATED / self.mod_name / 'Mods' / self.mod_name
        self.mod_localization_path = self.mod_translated_path / 'Localization' / str(self.target_language_name).replace(' ', '')
        self.mod_localization_path.mkdir(parents=True, exist_ok=True)

    
    def _create_meta(self) -> None:
        LsxParser.create_meta(
            mod_name=self.mod_name,
            meta_file_path=self.meta_path,
            meta_output_path=(self.mod_translated_path / 'meta.lsx'),
            author=self.author,
            description=self.description,
        )

    
    def _translate(self) -> None:
        for xml_path in self.xml_paths:
            localization = XmlParser.xml_to_dataframe(xml_path)
            
            if localization.empty:
                print(f'{xml_path.name} não possui content.')
                xml_path.unlink()
                continue
            
            try:
                self._translate_xml_files(localization)
            except KeyError as e:
                print(f'{xml_path.name} não possui content.')
                xml_path.unlink()
                continue

            xml_output_path = self.mod_localization_path / xml_path.name
            XmlParser.dataframe_to_xml(localization, xml_output_path)


    def _translate_xml_files(self, localization: pd.DataFrame) -> None:
        total_rows = len(localization)
        counter = 0
        gpt_calls = 0
        for idx, row in localization.iterrows():

            source_text = row['text']
            contentuid = row['contentuid']

            target_text = DictionaryRepository.find_translations_by_text(
                session=self.session,
                source_lang=self.source_language,
                target_lang=self.target_language,
                source_text=source_text,
            )

            if target_text is None:

                prompt = self.openai_prompt.get_prompt(
                    source_text=source_text,
                )

                target_text = self.openai_service.gpt_chat_completion(
                    content=source_text,
                    system_prompt=prompt,
                )

            DictionaryRepository.upsert_translation(
                session=self.session,
                source_lang=self.source_language,
                target_lang=self.target_language,
                source_text=source_text,
                target_text=target_text,
                mod_name=self.mod_name,
                uid=contentuid,
            )

            localization.at[idx, 'text'] = target_text

            counter += 1
            print(f'Translation progress: {counter}/{total_rows}')
