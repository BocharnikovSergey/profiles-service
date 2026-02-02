import pytest
from fastapi.testclient import TestClient
from main import app
import pytest
from alembic.config import Config
import pytest
from alembic import command
from config import settings

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c



@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")
    yield