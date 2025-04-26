from sqlmodel import Session, select
from sqlmodel.sql.expression import Select

from ..models.language import Language


class LanguageRepository:

    @staticmethod
    def find_language_by_code(session: Session, code: str) -> str:
        statement = select(Language).where(Language.code == code)
        return str(session.exec(statement).first().name)
    
    @staticmethod
    def find_language_by_name(session: Session, name: str) -> str:
        statement = select(Language).where(Language.name == name)
        return str(session.exec(statement).first().code)
    
    @staticmethod
    def get_all_language_names(session: Session) -> list[str]:
        statement = select(Language.name)
        return sorted(session.exec(statement).all())
    
    @staticmethod
    def get_all_language_codes(session: Session) -> list[str]:
        statement = select(Language.code)
        return sorted(session.exec(statement).all())
