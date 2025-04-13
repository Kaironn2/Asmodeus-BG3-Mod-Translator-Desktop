from sqlmodel import SQLModel, create_engine

from .models import Dictionary, Language, Mod
from .seeds.seed_languages import seed_languages


engine = create_engine(
    'sqlite:///data/db/dictionary.db',
    echo=False,
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine, checkfirst=True)
    seed_languages(engine=engine)
