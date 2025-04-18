from src.database.connection import create_db_and_tables, get_session
from src.pipelines.openai_translation import OpenAITranslationPipeline
from src.helpers.validators import Validators


if __name__ == "__main__":
    create_db_and_tables()

    mod_name = 'Cosmic sorcery'

    with get_session() as session:
        openai_translation_pipeline = OpenAITranslationPipeline(
            mod_name=mod_name,
            session=session,
            source_language='en',
            target_language='ptbr',
            author='Kaironn2',
            description='Cosmic Sorcery PTBR Translation',
            mod_path='C:\\Users\\jonat\\Desktop\\projects\\Asmodeus-Translator-Desktop\\CosmicSorcery.zip'
        )
        openai_translation_pipeline.run()
