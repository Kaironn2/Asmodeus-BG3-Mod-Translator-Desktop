from sqlmodel import Session, select

from ..models import Language


languages = [
    {'code': 'en', 'name': 'English'},
    {'code': 'ptbr', 'name': 'Brazilian Portuguese'},
    {'code': 'pt', 'name': 'Portuguese'},
    {'code': 'es', 'name': 'Spanish'},
    {'code': 'fr', 'name': 'French'},
    {'code': 'de', 'name': 'German'},
    {'code': 'it', 'name': 'Italian'},
    {'code': 'nl', 'name': 'Dutch'},
    {'code': 'sv', 'name': 'Swedish'},
    {'code': 'da', 'name': 'Danish'},
    {'code': 'no', 'name': 'Norwegian'},
    {'code': 'fi', 'name': 'Finnish'},
    {'code': 'ru', 'name': 'Russian'},
    {'code': 'uk', 'name': 'Ukrainian'},
    {'code': 'pl', 'name': 'Polish'},
    {'code': 'cs', 'name': 'Czech'},
    {'code': 'sk', 'name': 'Slovak'},
    {'code': 'hu', 'name': 'Hungarian'},
    {'code': 'ro', 'name': 'Romanian'},
    {'code': 'bg', 'name': 'Bulgarian'},
    {'code': 'el', 'name': 'Greek'},
    {'code': 'tr', 'name': 'Turkish'},
    {'code': 'he', 'name': 'Hebrew'},
    {'code': 'ar', 'name': 'Arabic'},
    {'code': 'fa', 'name': 'Persian'},
    {'code': 'hi', 'name': 'Hindi'},
    {'code': 'bn', 'name': 'Bengali'},
    {'code': 'ur', 'name': 'Urdu'},
    {'code': 'ta', 'name': 'Tamil'},
    {'code': 'te', 'name': 'Telugu'},
    {'code': 'ml', 'name': 'Malayalam'},
    {'code': 'zh', 'name': 'Chinese'},
    {'code': 'zh-tw', 'name': 'Traditional Chinese'},
    {'code': 'ja', 'name': 'Japanese'},
    {'code': 'ko', 'name': 'Korean'},
    {'code': 'vi', 'name': 'Vietnamese'},
    {'code': 'th', 'name': 'Thai'},
    {'code': 'id', 'name': 'Indonesian'},
    {'code': 'ms', 'name': 'Malay'},
    {'code': 'fil', 'name': 'Filipino'},
    {'code': 'sw', 'name': 'Swahili'},
    {'code': 'am', 'name': 'Amharic'},
    {'code': 'yo', 'name': 'Yoruba'},
    {'code': 'zu', 'name': 'Zulu'},
    {'code': 'xh', 'name': 'Xhosa'},
    {'code': 'af', 'name': 'Afrikaans'},
    {'code': 'sq', 'name': 'Albanian'},
    {'code': 'sr', 'name': 'Serbian'},
    {'code': 'hr', 'name': 'Croatian'},
]

languages_sorted = sorted(languages, key=lambda x: x['code'])

def seed_languages(engine):
    with Session(engine) as session:
        statement_check = select(Language)
        first_language = session.exec(statement_check).first()

        if not first_language:
            print('Seeding languages...')
            for lang in languages_sorted:
                db_lang = Language(code=lang['code'], name=lang['name'])
                session.add(db_lang)
            session.commit()
            print('Languages seeded.')


if __name__ == '__main__':
    seed_languages()
