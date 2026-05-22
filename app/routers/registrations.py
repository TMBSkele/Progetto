from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException

from app.data.db import get_session
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.get("/", response_model=list[Registration])
def get_registrations(
    session: Session = Depends(get_session),
) -> list[Registration]:
    """Restituisce la lista di tutte le registrazioni."""

    return session.exec(select(Registration)).all()


@router.delete("/")
def delete_registration(
    username: str,
    event_id: int,
    session: Session = Depends(get_session),
) -> dict[str, str]:
    """Elimina una registrazione identificata da username ed event_id."""

    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    registration = session.get(Registration, (username, event_id))

    if registration is None:
        raise HTTPException(status_code=404, detail="Registrazione non trovata")

    session.delete(registration)
    session.commit()

    return {"message": "Registrazione eliminata con successo"}