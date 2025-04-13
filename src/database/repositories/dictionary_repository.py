from typing import Optional, List
from sqlmodel import Session, select
from sqlmodel.sql.expression import Select

from ..helpers import DatabaseHelper
from ..models import Dictionary


class DictionaryRepository:

    @staticmethod
    def _get_ordered_inputs(
        source_lang: str, 
        target_lang: str, 
        source_text: str = None,
        target_text: str = None,
    ) -> List[str]:

        db_lang1, db_lang2 = sorted([source_lang, target_lang])

        if source_lang == db_lang1:

            if target_text is None:
                return db_lang1, db_lang2, source_text
            
            if source_text is None:
                return db_lang1, db_lang2
            
            return db_lang1, db_lang2, source_text, target_text
            
        if source_lang == db_lang2:
            
            if target_text is None:
                return db_lang1, db_lang2, source_text
            
            if source_text is None:
                return db_lang1, db_lang2
            
            return db_lang1, db_lang2, source_text, target_text
            
    
    @classmethod
    def find_translations_by_text(
        cls,
        source_lang: str,
        target_lang: str,
        source_text: str,
    ) -> Select[Dictionary]:
        
        db_lang1, db_lang2, source_text = cls._get_ordered_inputs(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
        )

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
        
        db_lang1, db_lang2 = cls._get_ordered_inputs(
            source_lang=source_lang,
            target_lang=target_lang,
        )

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
        
        db_lang1, db_lang2 = cls._get_ordered_inputs(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
        )

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
        
        db_lang1, db_lang2, text1, text2 = cls._get_ordered_inputs(
            source_lang, target_lang, source_text, target_text
        )

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
        if result:
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
