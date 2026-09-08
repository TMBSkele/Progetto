from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """Rappresenta un utente registrato nel sistema."""

    username: str = Field(primary_key=True)
    name: str
    email: str