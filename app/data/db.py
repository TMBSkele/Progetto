from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
# TODO: remember to import all the DB models here
from app.models.registration import Registration  # NOQA
from app.models.event import Event
from app.models.user import User


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    """Crea le tabelle del database e inizializza eventuali dati iniziali."""
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            # TODO: (optional) initialize the database with fake data
            ...


def get_session():
    """Fornisce una sessione SQLModel alle dipendenze FastAPI."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
