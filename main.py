from src.database.connection import create_db_and_tables, get_session
from src.database.repositories.dictionary_repository import DictionaryRepository
from src.services.openai.prompts import OpenAIPrompt
from src.services.openai.openai_service import OpenAIService
from src.parsers.lsx_parser import LsxParser


if __name__ == "__main__":
    create_db_and_tables()

    # with get_session() as session:
    #     DictionaryRepository.upsert_translation(
    #         session=session,
    #         source_lang='en',
    #         target_lang='ptbr',
    #         source_text='Fireball',
    #         target_text='Bola de Fogo',
    #         mod_name='test_mod2',
    #     )

    # prompter = OpenAIPrompt(source_lang='en', target_lang='ptbr', session=session)
    # print(prompter.get_prompt(
    #     source_text='Fire Stick',
    # ))

    # openai_service = OpenAIService()
    # result = openai_service.gpt_chat_completion(
    #     content='Fire Stick',
    #     system_prompt=prompter.get_prompt(source_text='Fire Stick')
    # )
    # print(result)


    LsxParser.create_meta(
        meta_file_path='C:\\Users\\jonat\\Desktop\\bg3-mod-translator\\modders_multitools\\UnpackedMods\\AdditionalEnemies\\Mods\\AdditionalEnemies\\meta.lsx',
        meta_output_path='C:\\Users\\jonat\\Desktop\\bg3-mod-translator\\modders_multitools\\UnpackedMods\\AdditionalEnemies\\Mods\\AdditionalEnemies\\meta2.lsx',
        author='Kaironn2',
        description='Additional_ptbr',
        target_lang='ptbr',
    )