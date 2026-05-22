from sqlmodel import Field, SQLModel


class Registration(SQLModel, table=True):
    """Modello ORM per rappresentare la registrazione di un utente a un evento."""

    username: str = Field(foreign_key="user.username", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)