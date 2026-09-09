from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.registration import Registration
from app.models.user import User, UserCreate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_users(session: SessionDep) -> list[User]:
    """Restituisce la lista di tutti gli utenti."""

    return list(session.exec(select(User)).all())


@router.post("", status_code=201)
def create_user(user_data: UserCreate, session: SessionDep) -> User:
    """Crea un nuovo utente."""

    existing_user = session.get(User, user_data.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="User already exists",
        )

    user = User.model_validate(user_data)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/{username}")
def get_user(username: str, session: SessionDep) -> User:
    """Restituisce un utente tramite username."""

    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("")
def delete_users(session: SessionDep) -> str:
    """Elimina tutti gli utenti e tutte le registrazioni associate."""

    registrations = session.exec(select(Registration)).all()
    users = session.exec(select(User)).all()

    for registration in registrations:
        session.delete(registration)

    for user in users:
        session.delete(user)

    session.commit()

    return "All users deleted successfully"


@router.delete("/{username}")
def delete_user(username: str, session: SessionDep) -> str:
    """Elimina un utente e tutte le sue registrazioni."""

    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(user)
    session.commit()

    return "User deleted successfully"