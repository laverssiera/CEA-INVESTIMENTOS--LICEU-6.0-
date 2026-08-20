from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.canonical_config import resolve_canonical_database

database_config = resolve_canonical_database()
DATABASE_URL = database_config.url

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": f"-csearch_path={database_config.schema}"},
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
