from uuid import UUID

from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.models.user import User


password_hash = PasswordHash.recommended()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, name: str, email: str, password: str):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise ValueError("Email address is already registered.")

    hashed_password = password_hash.hash(password)

    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role="school_owner"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user using their email and password.

    Returns the user if credentials are valid and the account is active.
    Otherwise, returns None.
    """

    user = get_user_by_email(db, email)

    if not user:
        return None

    password_is_valid = password_hash.verify(
        password,
        user.password_hash
    )

    if not password_is_valid:
        return None

    if not user.is_active:
        return None

    return user