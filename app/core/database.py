from sqlmodel import create_engine, Session
from typing import Generator
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():

    pass

def get_session() -> Generator[Session, None, None]:

    with Session(engine) as session:
        yield session