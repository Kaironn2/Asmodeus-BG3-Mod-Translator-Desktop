from sqlmodel import Session
from typing import Any, List

class DatabaseHelper:
    
    @staticmethod
    def add_and_commit(session: Session, obj: Any) -> None:
        session.add(obj)
        session.commit()
