from sqlmodel import Session, SQLModel, create_engine

from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration

DATABASE_URL = "sqlite:///app/data/database.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """Crea il database e le tabelle se non esistono già."""

    SQLModel.metadata.create_all(engine)


def get_session():
    """Restituisce una sessione database utilizzabile dalle API."""

    with Session(engine) as session:
        yield session