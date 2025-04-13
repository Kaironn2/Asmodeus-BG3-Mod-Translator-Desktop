from datetime import datetime

from sqlalchemy import func
from sqlmodel import SQLModel, Field


class Mod(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)

    created_at: datetime = Field(
    sa_column_kwargs={'server_default': func.now()}, nullable=False
    )
    updated_at: datetime = Field(
        sa_column_kwargs={'server_default': func.now(), 'onupdate': func.now()},
        nullable=False
    )
