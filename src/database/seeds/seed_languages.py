from sqlmodel import Session, select

from ..models import Language


languages = [
    {'code': 'ar', 'name': 'Arabic'},
    {'code': 'bg', 'name': 'Bulgarian'},
    {'code': 'cs', 'name': 'Czech'},
    {'code': 'da', 'name': 'Danish'},
    {'code': 'de', 'name': 'German'},
    {'code': 'el', 'name': 'Greek'},
    {'code': 'en', 'name': 'English'},
    {'code': 'es', 'name': 'Spanish'},
    {'code': 'et', 'name': 'Estonian'},
    {'code': 'fi', 'name': 'Finnish'},
    {'code': 'fr', 'name': 'French'},
    {'code': 'hu', 'name': 'Hungarian'},
    {'code': 'id', 'name': 'Indonesian'},
    {'code': 'it', 'name': 'Italian'},
    {'code': 'ja', 'name': 'Japanese'},
    {'code': 'ko', 'name': 'Korean'},
    {'code': 'lt', 'name': 'Lithuanian'},
    {'code': 'lv', 'name': 'Latvian'},
    {'code': 'nb', 'name': 'Norwegian Bokmål'},
    {'code': 'nl', 'name': 'Dutch'},
    {'code': 'pl', 'name': 'Polish'},
    {'code': 'pt', 'name': 'Portuguese'},
    {'code': 'pt-BR', 'name': 'Brazilian Portuguese'},
    {'code': 'ro', 'name': 'Romanian'},
    {'code': 'ru', 'name': 'Russian'},
    {'code': 'sk', 'name': 'Slovak'},
    {'code': 'sl', 'name': 'Slovenian'},
    {'code': 'sv', 'name': 'Swedish'},
    {'code': 'tr', 'name': 'Turkish'},
    {'code': 'uk', 'name': 'Ukrainian'},
    {'code': 'zh', 'name': 'Chinese'},
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
