from sqlalchemy.orm import Session
from src.database.models import User
from src.auth.security import hash_password, verify_password
from src.storage.credits import get_current_us_month

def create_local_user (
    db: Session,
    email: str,
    password: str,
):
    "Sign up a user with email and password"
    existing_user = db.query(User).filter (
        User.email == email
    ).first()

    if existing_user:
        raise ValueError("Email is already registered")

    db_user = User (
        email = email,
        hashed_password = hash_password(password),
        auth_provider = "local",
        free_credits = 20,
        purchased_credits = 0,
        last_reset_month = get_current_us_month()
    )

    db.add(db_user)
    db.commit()
    db.refresh (db_user)
    return db_user

def authenticate_local_user (
    db: Session,
    email: str,
    password: str,
):
    user = db.query(User).filter (
        User.email == email,
        User.auth_provider == "local"
    ).first()

    if not user or not verify_password(
        password, user.hashed_password
    ):
        raise ValueError("Invalid email or wrong password")
    return user

def register_or_login_google_user (
    db: Session, email: str
):
    user = db.query (User).filter (
        User.email == email,
        User.auth_provider == "google"
    ).first()

    if not user:
        user = User (
            email = email,
            auth_provider = "google",
            free_credits = 20,
            purchased_credits = 0,
            last_reset_month = get_current_us_month()
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    return user
 