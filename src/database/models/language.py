from sqlmodel import SQLModel, Field


class Language(SQLModel, table=True):
    id: int = Field(primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str
