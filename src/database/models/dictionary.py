from pydantic import model_validator
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class Dictionary(SQLModel, table=True):
    id: int = Field(primary_key=True)

    language1: str = Field(index=True, foreign_key='language.code')
    language2: str = Field(index=True, foreign_key='language.code')

    text_language1: str = Field(nullable=False)
    text_language2: str = Field(nullable=False)

    mod_name: str = Field(index=True, foreign_key='mod.name')
    uid: Optional[str] = Field(default=None, index=True, unique=True)


    __table_args__ = (
        Index('idx_dict_lang1_lang2_text1', 'language1', 'language2', 'text_language1'),
        Index('idx_dict_lang1_lang2_text2', 'language1', 'language2', 'text_language2'),
        Index('idx_dict_lang1_lang2_mod', 'language1', 'language2', 'mod_name'),
        Index('idx_dict_lang1_lang2_uid', 'language1', 'language2', 'uid'),
    )

    @model_validator(mode='before')
    @classmethod
    def sort_languages(cls, values: dict):
        l1, l2 = values.get('language1'), values.get('language2')
        if l1 and l2 and l1 > l2:
            values['language1'], values['language2'] = l2, l1
            values['text_language1'], values['text_language2'] = values['text_language2'], values['text_language1']
        return values
