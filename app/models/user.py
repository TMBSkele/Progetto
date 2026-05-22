from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Modello ORM per rappresentare un utente."""

    username: str = Field(primary_key=True)
    name: str
    email: str