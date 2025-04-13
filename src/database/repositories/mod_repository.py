from sqlmodel import Session, select
from sqlmodel.sql.expression import Select

from ..models.mods import Mod
from ..helpers import DatabaseHelper


class ModRepository:

    @classmethod
    def find_mod_by_name(cls, name: str) -> Select[Mod]:
        return select(Mod).where(Mod.name == name)


    @classmethod
    def find_all_mods(cls) -> Select[Mod]:
        return select(Mod).order_by(Mod.name)
    

    @classmethod
    def add_mod(cls, session: Session, name: str) -> Mod:
        statement = cls.find_mod_by_name(name=name)
        existing_mod = session.exec(statement).first()
        if existing_mod:
            return existing_mod
        
        mod = Mod(name=name)
        DatabaseHelper.add_and_commit(session=session, obj=mod)
        return mod