from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event

from .models import Dictionary, Language, Mod
from .seeds.seed_languages import seed_languages



engine = create_engine(
    'sqlite:///data/db/dictionary.db',
    echo=False,
)

@event.listens_for(engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine, checkfirst=True)
    seed_languages(engine=engine)


def get_session() -> SQLModel:
    return Session(engine, expire_on_commit=False)
