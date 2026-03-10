from sqlalchemy.orm import sessionmaker, Session
from common.logger import logger
from database.engine import engine


log = logger("database")


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    db = SessionLocal()
    log.debug("Database session opened")
    try:
        yield db
    except Exception as e:
        log.error(f"Database session error: {str(e)}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()
        log.debug("Database session closed")