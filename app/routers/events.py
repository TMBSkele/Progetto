from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event, EventCreate, EventUpdate
from app.models.user import User, UserCreate
from app.models.registration import Registration


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

@router.post("/{id}/register", status_code=201)
def register_user_to_event(
    id: int,
    user_data: UserCreate,
    session: SessionDep,
) -> str:
    """Registra un utente a un evento, creando l'utente se non esiste."""

    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    existing_user = session.get(User, user_data.username)

    if existing_user is None:
        user = User.model_validate(user_data)
        session.add(user)
        session.commit()

    registration = session.get(
        Registration,
        (user_data.username, id),
    )

    if registration is not None:
        raise HTTPException(
            status_code=400,
            detail="User already registered for this event",
        )

    new_registration = Registration(
        username=user_data.username,
        event_id=id,
    )

    session.add(new_registration)
    session.commit()

    return "User registered successfully"

@router.delete("")
def delete_events(session: SessionDep) -> str:
    """Elimina tutti gli eventi e tutte le registrazioni associate."""

    registrations = session.exec(select(Registration)).all()
    events = session.exec(select(Event)).all()

    for registration in registrations:
        session.delete(registration)

    for event in events:
        session.delete(event)

    session.commit()

    return "All events deleted successfully"

@router.delete("/{id}")
def delete_event(id: int, session: SessionDep) -> str:
    """Elimina un evento e tutte le registrazioni associate."""

    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    registrations = session.exec(
        select(Registration).where(Registration.event_id == id)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(event)
    session.commit()

    return "Event deleted successfully"