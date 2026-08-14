from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
import os

DATABASE_DIR = './data'
os.makedirs (DATABASE_DIR, exist_ok=True)
DATABASE_URL = f"sqlite:///{DATABASE_DIR}/app.db"

engine = create_engine (
    DATABASE_URL,
    connect_args = {'check_same_thread': False}
    # Required for SQLite when I use Fast APi
)

SessionLocal = sessionmaker (
    autocommit = False,
    autoflush = False,
    bind = engine,
)

# This function is for initializing a database
def init_db():
    Base.metadata.create_all (bind = engine)

# This function is to fetch the database
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close() #always close after yield to prevent leaking addresses