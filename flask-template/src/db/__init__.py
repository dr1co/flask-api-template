"""Database engine and session management.

Holds the SQLAlchemy engine/session setup used to talk to relational
databases (e.g. MSSQL via ODBC). Call init_engine(DATABASE_URL) once at
app startup and then use get_session() as a context manager for queries.
This is a plain engine/session layer, not an ORM model layer -- put
models in src/schemas or src/classes as the project requires.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_engine = None
_SessionLocal = None


def init_engine(database_url: str):
    global _engine, _SessionLocal

    if not database_url:
        return

    _engine = create_engine(database_url, pool_pre_ping=True)
    _SessionLocal = sessionmaker(
        bind=_engine, autoflush=False, autocommit=False
    )


@contextmanager
def get_session():
    if _SessionLocal is None:
        raise RuntimeError(
            "Database engine is not configured. "
            "Set DATABASE_URL and call init_engine()."
        )

    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
