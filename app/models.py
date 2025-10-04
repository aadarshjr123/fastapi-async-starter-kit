from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./users.db"  # keep as-is
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


Base.metadata.create_all(bind=engine)


# Explaination:
# This code defines a SQLAlchemy model for a User and sets up a SQLite database connection.
# The User model has three fields: id, name, and email.
# The database is created in a file named users.db, and the users table is created if it doesn't exist.
# The SessionLocal class is used to create database sessions for interacting with the database.
# The declarative_base function is used to create a base class for the model.
# The create_engine function sets up the connection to the SQLite database.
# The connect_args parameter is used to allow multiple threads to access the database.
# The metadata.create_all method is called to create the users table in the database.
