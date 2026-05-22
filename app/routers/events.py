from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from app.data.db import get_session
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=list[Event])
def get_events(session: Session = Depends(get_session)) -> list[Event]:
    """Restituisce la lista di tutti gli eventi."""

    return session.exec(select(Event)).all()


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: Event, session: Session = Depends(get_session)) -> Event:
    """Crea un nuovo evento."""

    event.id = None
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int, session: Session = Depends(get_session)) -> Event:
    """Restituisce un evento tramite il suo ID."""

    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    return event


@router.put("/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    updated_event: Event,
    session: Session = Depends(get_session),
) -> Event:
    """Aggiorna un evento esistente."""

    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    event.title = updated_event.title
    event.description = updated_event.description
    event.date = updated_event.date
    event.location = updated_event.location

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@router.post("/{event_id}/register", status_code=status.HTTP_201_CREATED)
def register_user_to_event(
    event_id: int,
    user: User,
    session: Session = Depends(get_session),
) -> dict[str, str]:
    """Registra un utente a un evento, creando l'utente se non esiste."""

    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    existing_user = session.get(User, user.username)

    if existing_user is None:
        session.add(user)
        session.commit()

    existing_registration = session.get(
        Registration,
        (user.username, event_id),
    )

    if existing_registration is not None:
        raise HTTPException(
            status_code=400,
            detail="Utente già registrato a questo evento",
        )

    registration = Registration(username=user.username, event_id=event_id)

    session.add(registration)
    session.commit()

    return {"message": "Registrazione effettuata con successo"}


@router.delete("/")
def delete_events(session: Session = Depends(get_session)) -> dict[str, str]:
    """Elimina tutti gli eventi e tutte le registrazioni associate."""

    registrations = session.exec(select(Registration)).all()
    events = session.exec(select(Event)).all()

    for registration in registrations:
        session.delete(registration)

    for event in events:
        session.delete(event)

    session.commit()

    return {"message": "Tutti gli eventi sono stati eliminati"}


@router.delete("/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    """Elimina un evento e tutte le registrazioni associate."""

    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    registrations = session.exec(
        select(Registration).where(Registration.event_id == event_id)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(event)
    session.commit()

    return {"message": "Evento eliminato con successo"}