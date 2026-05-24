from datetime import datetime
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    """Modello ORM per rappresentare un evento."""

    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str