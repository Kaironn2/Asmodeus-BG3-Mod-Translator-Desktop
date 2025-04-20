from typing import Optional, List
from sqlmodel import Session, select
from sqlmodel.sql.expression import Select

from src.helpers.fuzzy_matcher import SimilarFinder

from src.database.helpers import DatabaseHelper
from src.database.models import Dictionary
from src.database.repositories.mod_repository import ModRepository


class DictionaryRepository:

    @classmethod
    def find_all_translations_by_language(
        cls,
        source_lang: str,
        target_lang: str,
    ) -> Select[Dictionary]:
        
        db_lang1, db_lang2 = sorted([source_lang, target_lang])

        return select(Dictionary).where(
            Dictionary.language1 == db_lang1,
            Dictionary.language2 == db_lang2,
        ).order_by(Dictionary.text_language1)

    
    @classmethod
    def find_translations_by_text(
        cls,
        session: Session,
        source_language: str,
        target_language: str,
        source_text: str,
    ) -> str:
        
        db_lang1, db_lang2 = sorted([source_language, target_language])

        statement = select(Dictionary).where(
            Dictionary.language1 == db_lang1,
            Dictionary.language2 == db_lang2,
            Dictionary.text_language1 == source_text,
        )

        result = session.exec(statement).first()
        if result:
            return result.text_language2
        return None
    

    @classmethod
    def find_translations_by_uid(
        cls,
        session: Session,
        source_language: str,
        target_language: str,
        uid: str,
    ) -> Select[Dictionary]:
        
        db_lang1, db_lang2 = sorted([source_language, target_language])

        statement = select(Dictionary).where(
            Dictionary.language1 == db_lang1,
            Dictionary.language2 == db_lang2,
            Dictionary.uid == uid,
        )

        return session.exec(statement).first()
    

    @classmethod
    def find_translations_by_mod(
        cls,
        session: Session,
        source_language: str,
        target_language: str,
        source_text: str,
        mod_name: str,
    ) -> Select[Dictionary]:
        
        db_lang1, db_lang2 = sorted([source_language, target_language])

        statement = select(Dictionary).where(
            Dictionary.language1 == db_lang1,
            Dictionary.language2 == db_lang2,
            Dictionary.text_language1 == source_text,
            Dictionary.mod_name == mod_name,
        )
        return session.exec(statement).first()
    

    @classmethod
    def upsert_translation(
        cls,
        session: Session,
        source_language: str,
        target_language: str,
        source_text: str,
        target_text: str,
        mod_name: str,
        uid: Optional[str] = None,
    ) -> None:
        
        ModRepository.add_mod(session=session, name=mod_name)
        
        db_lang1, db_lang2 = sorted([source_language, target_language])

        if target_language == db_lang1:
            text1, text2 = target_text, source_text
        text1, text2 = source_text, target_text


        if uid:
            result = cls.find_translations_by_uid(session, source_language, target_language, uid)
            if result:
                result.text_language1 = text1
                result.text_language2 = text2
                session.commit()
                return

        result = cls.find_translations_by_mod(session, source_language, target_language, source_text, mod_name)
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
    

    @classmethod
    def find_similar_translations(
        cls,
        session: Session,
        source_lang: str,
        target_lang: str,
        source_text: str,
    ) -> List[tuple[str, str]]:
        
        db_lang1, db_lang2 = sorted([source_lang, target_lang])
        results = session.exec(
            cls.find_all_translations_by_language(db_lang1, db_lang2)
        )

        db_texts = {result.text_language1: result.text_language2 for result in results}

        result = SimilarFinder.search_similar_texts(
            source_text=source_text,
            db_texts=db_texts,
        )

        return result


    @classmethod
    def get_all_mod_names(
        cls,
        session: Session,
    ) -> List[str]:
        
        statement = select(Dictionary.mod_name).distinct()
        result = session.exec(statement).all()
        return result
    
    @classmethod
    def get_entries_by_mod(
        cls,
        session: Session,
        mod_name: str,
    ) -> list[dict]:
        statement = select(Dictionary).where(
            Dictionary.mod_name == mod_name,
        )
        results = session.exec(statement).all()
        return [
            {
                'text_language1': entry.text_language1,
                'text_language2': entry.text_language2,
                'uid': entry.uid,
                'language1': entry.language1,
                'language2': entry.language2,
                'mod_name': entry.mod_name,
            }
            for entry in results
        ]
