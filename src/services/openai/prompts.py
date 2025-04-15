from src.database.repositories.dictionary_repository import DictionaryRepository
from sqlmodel import Session


class OpenAIPrompt:

    def __init__(self, source_lang: str, target_lang: str, session: Session):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.session = session


    def get_prompt(self, source_text: str) -> str:
        context = self._build_context(source_text)
        return self._build_prompt(context)


    def _build_context(self, source_text: str) -> str:
        results = DictionaryRepository.find_similar_translations(
            session=self.session,
            source_lang=self.source_lang,
            target_lang=self.target_lang,
            source_text=source_text,
        )
        return '\n'.join(
           f'{list(result.keys())[0]} -> {list(result.values())[0]}' for result in results
        )


    def _build_prompt(self, context: str) -> str:
        return (
            f'You are a translator specialized in video game localization, translating from {self.source_lang} to {self.target_lang}. '
            f'You have been hired to specifically translate content from the game Baldur\'s Gate 3. '
            f'You may also use terminology from Dungeons & Dragons, such as "d20", "d8", "dungeon master", etc. '
            f'Follow these critical rules:\n'
            f'1. DO NOT translate variable names, tags, or placeholders (such as [Player], <CHAR>, {{0}}, etc.)\n'
            f'2. You will encounter tags in the following format -> &lt;LSTag Type="Status" Tooltip="BLINDED"&gt;Blinded&lt;/LSTag&gt;. Only translate "Blinded". DO NOT change the tag.\n'
            f'3. Keep all original formatting (spacing, line breaks)\n'
            f'4. Preserve all special characters and punctuation\n'
            f'5. Adapt idiomatic expressions to sound natural in the target language\n'
            f'6. Only translate the text that would be visible to the player\n'
            f'7. Return ONLY the translated text, no explanations\n'
            f'8. Translate inner LSTAG content: AttackRoll = "Attack Roll", SavingThrow = "Saving Throw", AbilityCheck = "Ability Check"\n\n'
            f'Obs: in brazilian portuguese: "Saving Throw" = "Teste de Resistência", "Attack Roll" = "Rolagem de Ataque", "Ability Check" = "Teste de Habilidade"\n\n'
            f'{context}'
        )
