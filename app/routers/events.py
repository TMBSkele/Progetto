from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User


router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[Event])
def get_events(session: SessionDep) -> list[Event]:
    """Restituisce la lista di tutti gli eventi."""

    return list(session.exec(select(Event)).all())


@router.post("", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: Event, session: SessionDep) -> Event:
    """Crea un nuovo evento."""

    event.id = None
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/{id}", response_model=Event)
def get_event(id: int, session: SessionDep) -> Event:
    """Restituisce un evento tramite ID."""

    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.put("/{id}", response_model=Event)
def update_event(id: int, updated_event: Event, session: SessionDep) -> Event:
    """Aggiorna un evento esistente."""

    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = updated_event.title
    event.description = updated_event.description
    event.date = updated_event.date
    event.location = updated_event.location

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@router.post("/{id}/register", status_code=status.HTTP_201_CREATED)
def register_user_to_event(id: int, user: User, session: SessionDep) -> str:
    """Registra un utente a un evento, creando l'utente se non esiste."""

    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    existing_user = session.get(User, user.username)

    if existing_user is None:
        session.add(user)
        session.commit()

    registration = session.get(Registration, (user.username, id))

    if registration is not None:
        raise HTTPException(
            status_code=400,
            detail="User already registered for this event",
        )

    new_registration = Registration(username=user.username, event_id=id)
    session.add(new_registration)
    session.commit()

    return "User registered successfully"


@router.delete("")
def delete_events(session: SessionDep) -> str:
    """Elimina tutti gli eventi e le registrazioni associate."""

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
    """Elimina un evento e le registrazioni associate."""

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