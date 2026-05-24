from typing import Annotated
import os

from fastapi import Depends
from faker import Faker
from sqlmodel import Session, SQLModel, create_engine

from app.config import config
from app.models.event import Event  # NOQA
from app.models.user import User  # NOQA
from app.models.registration import Registration  # NOQA


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    """Crea le tabelle del database se non esistono già."""

    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)

    if not ds_exists:
        Faker("it_IT")


def get_session():
    """Restituisce una sessione database per le API."""

    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]