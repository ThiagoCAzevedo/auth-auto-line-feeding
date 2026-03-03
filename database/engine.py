from sqlalchemy import create_engine, event
from sqlalchemy.pool import Pool
from common.logger import logger
from config.settings import settings


log = logger("database")


DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{settings.MYSQL_USER}:{settings.MYSQL_PSWD}@"
    f"{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/"
    f"{settings.MYSQL_DATABASE}"
)

log.info(f"Initializing database connection: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    
    @event.listens_for(Pool, "connect")
    def receive_connect(dbapi_conn, connection_record):
        log.debug("Database connection established")
    
    @event.listens_for(Pool, "close")
    def receive_close(dbapi_conn, connection_record):
        log.debug("Database connection closed")
    
    log.info("Database engine initialized successfully")

except Exception as e:
    log.error(f"Failed to initialize database engine: {str(e)}", exc_info=True)
    raise