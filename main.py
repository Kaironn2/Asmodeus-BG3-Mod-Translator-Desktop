from src.database.connection import create_db_and_tables, get_session
from src.pipelines.openai_translation import OpenAITranslationPipeline


if __name__ == "__main__":
    create_db_and_tables()

    with get_session() as session:
        openai_translation_pipeline = OpenAITranslationPipeline(
            mod_name='Chaos and Control - Sorcerer Equipment',
            session=session,
            source_language='en',
            target_language='ptbr',
            author='Kaironn2',
            description='Chaos and Control - Sorcerer Equipment',
            mod_path='C:\\Users\\jonat\\Desktop\\projects\\Asmodeus-Translator-Desktop\\Chaos and Control - Sorcerer Equipment-15116-1-0-0-6-1744837990.zip'
        )
        openai_translation_pipeline.run()
