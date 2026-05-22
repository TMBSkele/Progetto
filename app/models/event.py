from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    """Modello ORM per rappresentare un evento."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str