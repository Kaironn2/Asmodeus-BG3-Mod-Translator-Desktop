from datetime import datetime
from pydantic import model_validator
from typing import Optional

from sqlmodel import SQLModel, Field, UniqueConstraint
from sqlalchemy import Index
from sqlalchemy import func


class Dictionary(SQLModel, table=True):
    id: int = Field(primary_key=True)

    language1: str = Field(index=True, foreign_key='language.code')
    language2: str = Field(index=True, foreign_key='language.code')

    text_language1: str = Field(nullable=False)
    text_language2: str = Field(nullable=False)

    mod_name: str = Field(index=True, foreign_key='mod.name')
    uid: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(
    sa_column_kwargs={'server_default': func.now()}, nullable=False
    )
    updated_at: datetime = Field(
        sa_column_kwargs={'server_default': func.now(), 'onupdate': func.now()},
        nullable=False
    )


    __table_args__ = (
        Index('idx_dict_lang1_lang2_text1', 'language1', 'language2', 'text_language1'),
        Index('idx_dict_lang1_lang2_text2', 'language1', 'language2', 'text_language2'),
        Index('idx_dict_lang1_lang2_mod', 'language1', 'language2', 'mod_name'),
        Index('idx_dict_lang1_lang2_uid', 'language1', 'language2', 'uid'),
        UniqueConstraint('language1', 'language2', 'uid', name='uq_dict_lang1_lang2_uid'),
    )

    @model_validator(mode='before')
    @classmethod
    def sort_languages(cls, values: dict):
        l1, l2 = values.get('language1'), values.get('language2')
        l1_sorted, l2_sorted = sorted([l1, l2])
        
        if l1_sorted != l1:
            values['language1'], values['language2'] = l1_sorted, l2_sorted
            values['text_language1'], values['text_language2'] = values.get('text_language2'), values.get('text_language1')
            return values
