from datetime import datetime

from sqlmodel import SQLModel, Field


class EventBase(SQLModel):
    """Campi condivisi da un evento."""

    title: str
    description: str
    date: datetime
    location: str


class Event(EventBase, table=True):
    """Rappresenta un evento salvato nel database."""

    id: int | None = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    """Dati richiesti per la creazione di un evento."""

    pass

class EventUpdate(EventBase):
    """Dati richiesti per l'aggiornamento di un evento."""

    pass