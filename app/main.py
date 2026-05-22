from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.data.db import create_db_and_tables
from app.routers import events, users, registrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestisce le operazioni di startup dell'applicazione."""

    create_db_and_tables()
    yield


app = FastAPI(
    title="Event Management API",
    lifespan=lifespan,
)

app.include_router(events.router)
app.include_router(users.router)
app.include_router(registrations.router)