from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User (Base):
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key = True,
        index = True,
        nullable=False,
    )
    email = Column(
        String,
        unique = True,
        index = True,
        nullable = False,
    )
    hashed_password = Column (
        String,
        nullable=True, #passowrd is not needed for userse using Google Auth
    )
    auth_provider = Column (String, default = "local") # it's either local or from Google
    free_credits = Column (Integer, default = 40)
    purchased_credits = Column(Integer, default = 0)
    last_reset_month = Column (String, nullable=True)