from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database.base import Base
from database.session import get_db
from main import create_app
import sys, pytest


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def db_session():
    """Banco isolado para cada teste (SQLite em memória)"""

    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    db = SessionLocal()

    yield db

    db.close()
    engine.dispose()


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def client(app, db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client