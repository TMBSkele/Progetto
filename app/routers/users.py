from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from app.data.db import get_session
from app.models.user import User
from app.models.registration import Registration

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
def get_users(session: Session = Depends(get_session)) -> list[User]:
    """Restituisce la lista di tutti gli utenti."""

    return session.exec(select(User)).all()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User, session: Session = Depends(get_session)) -> User:
    """Crea un nuovo utente."""

    existing_user = session.get(User, user.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="Esiste già un utente con questo username",
        )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/{username}", response_model=User)
def get_user(username: str, session: Session = Depends(get_session)) -> User:
    """Restituisce un utente tramite username."""

    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    return user


@router.delete("/")
def delete_users(session: Session = Depends(get_session)) -> dict[str, str]:
    """Elimina tutti gli utenti e tutte le registrazioni associate."""

    registrations = session.exec(select(Registration)).all()
    users = session.exec(select(User)).all()

    for registration in registrations:
        session.delete(registration)

    for user in users:
        session.delete(user)

    session.commit()

    return {"message": "Tutti gli utenti sono stati eliminati"}


@router.delete("/{username}")
def delete_user(username: str, session: Session = Depends(get_session)) -> dict[str, str]:
    """Elimina un utente e tutte le sue registrazioni."""

    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(user)
    session.commit()

    return {"message": "Utente eliminato con successo"}