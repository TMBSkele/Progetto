from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """Campi condivisi da un utente."""

    username: str
    name: str
    email: str


class User(UserBase, table=True):
    """Rappresenta un utente registrato nel sistema."""

    username: str = Field(primary_key=True)


class UserCreate(UserBase):
    """Dati richiesti per la creazione di un utente."""

    pass