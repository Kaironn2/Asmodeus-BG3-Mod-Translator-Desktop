from sqlmodel import Session, select
from sqlmodel.sql.expression import Select

from ..models.language import Language


class LanguageRepository:

    @staticmethod
    def find_language_by_code(session: Session, code: str) -> str:
        statement = select(Language).where(Language.code == code)
        return str(session.exec(statement).first().name)
