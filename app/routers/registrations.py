from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User


router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.get("", response_model=list[Registration])
def get_registrations(session: SessionDep) -> list[Registration]:
    """Restituisce la lista di tutte le registrazioni."""

    return list(session.exec(select(Registration)).all())


@router.delete("")
def delete_registration(
    username: str,
    event_id: int,
    session: SessionDep,
) -> str:
    """Elimina una registrazione tramite username ed event_id."""

    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    registration = session.get(Registration, (username, event_id))

    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()

    return "Registration deleted successfully"