# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import app.config as config
from contextlib import contextmanager

Base = declarative_base()
engine = create_engine(config.DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, expire_on_commit=False, autoflush=False, bind=engine)


@contextmanager
def session_scope():
    session = SessionLocal()
    session.begin()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    else:
        session.commit()
    finally:
        session.close()
