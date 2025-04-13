from sqlmodel import SQLModel, Field


class Mod(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)
