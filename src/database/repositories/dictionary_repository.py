from typing import Optional, List
from sqlmodel import Session, select
from sqlmodel.sql.expression import Select

from ..helpers import DatabaseHelper
from ..models import Dictionary
from ..repositories.mod_repository import ModRepository


class DictionaryRepository:
    
    @classmethod
    def find_translations_by_text(
        cls,
        source_lang: str,
        target_lang: str,
        source_text: str,
    ) -> Select[Dictionary]:
        
        db_lang1, db_lang2 = sorted([source_lang, target_lang])

        return select(Dictionary).where(
            Dictionary.language1 == db_lang1,
            Dictionary.language2 == db_lang2,
            Dictionary.text_language1 == source_text,
        )
    

    @classmethod
    def find_translations_by_uid(
        cls,
        source_lang: str,
        target_lang: str,
        uid: str,
    ) -> Select[Dictionary]:
        
        db_lang1, db_lang2 = sorted([source_lang, target_lang])

        return select(Dictionary).where(
            Dictionary.language1 == db_lang1,
            Dictionary.language2 == db_lang2,
            Dictionary.uid == uid,
        )
    

    @classmethod
    def find_translations_by_mod(
        cls,
        source_lang: str,
        target_lang: str,
        source_text: str,
        mod_name: str,
    ) -> Select[Dictionary]:
        
        db_lang1, db_lang2 = sorted([source_lang, target_lang])

        return select(Dictionary).where(
            Dictionary.language1 == db_lang1,
            Dictionary.language2 == db_lang2,
            Dictionary.text_language1 == source_text,
            Dictionary.mod_name == mod_name,
        )
    

    @classmethod
    def upsert_translation(
        cls,
        session: Session,
        source_lang: str,
        target_lang: str,
        source_text: str,
        target_text: str,
        mod_name: str,
        uid: Optional[str] = None,
    ) -> None:
        
        ModRepository.add_mod(session=session, name=mod_name)
        
        db_lang1, db_lang2 = sorted([source_lang, target_lang])

        if target_lang == db_lang1:
            text1, text2 = target_text, source_text
        text1, text2 = source_text, target_text


        if uid:
            statement = cls.find_translations_by_uid(source_lang, target_lang, uid)
            result = session.exec(statement).first()
            if result:
                result.text_language1 = text1
                result.text_language2 = text2
                session.commit()
                return

        statement = cls.find_translations_by_mod(source_lang, target_lang, source_text, mod_name)
        result = session.exec(statement).first()
        if result and not uid:
            result.text_language1 = text1
            result.text_language2 = text2
            session.commit()
            return

        new_entry = Dictionary(
            language1=db_lang1,
            language2=db_lang2,
            text_language1=text1,
            text_language2=text2,
            mod_name=mod_name,
            uid=uid,
        )
        DatabaseHelper.add_and_commit(session, new_entry)
        return
