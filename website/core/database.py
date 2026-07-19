"""Database configuration and session management."""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import StaticPool
from app.core.config import get_settings

settings = get_settings()

# SQLite-specific args for threading
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
poolclass = StaticPool if settings.DATABASE_URL.startswith("sqlite") else None

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    poolclass=poolclass,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    """Yield a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
