from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event, EventCreate, EventUpdate


router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def get_events(session: SessionDep) -> list[Event]:
    """Restituisce la lista di tutti gli eventi presenti nel database."""
    events = session.exec(select(Event)).all()
    return events


@router.post("", status_code=201)
def create_event(event_data: EventCreate, session: SessionDep) -> Event:
    """Crea un nuovo evento e lo salva nel database."""
    event = Event.model_validate(event_data)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event

@router.get("/{id}")
def get_event(id: int, session: SessionDep) -> Event:
    """Restituisce un evento tramite il suo identificativo."""
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event

@router.put("/{id}")
def update_event(id: int, event_data: EventUpdate, session: SessionDep) -> Event:
    """Aggiorna un evento esistente."""

    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = event_data.title
    event.description = event_data.description
    event.date = event_data.date
    event.location = event_data.location

    session.add(event)
    session.commit()
    session.refresh(event)

    return event