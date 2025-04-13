from src.database.connection import create_db_and_tables, get_session
from src.database.repositories.dictionary_repository import DictionaryRepository


if __name__ == "__main__":
    create_db_and_tables()

    with get_session() as session:
        DictionaryRepository.upsert_translation(
            session=session,
            source_lang='en',
            target_lang='ptbr',
            source_text='Fire',
            target_text='Fogo',
            mod_name='test_mod2',
        )
