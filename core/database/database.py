#====================== IMPORTS ================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.pool import StaticPool

#================================================================

SQLALCHEMY_DATABASE_URL: str = "sqlite:///../db.sqlite3"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

"""
create base class for declaring tables
"""

Base = declarative_base()


#=================== CONNECTION TO MAIN.PY =====================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#================================================================