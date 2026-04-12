from collections.abc import Generator
import os
from pathlib import Path
import sys

import pytest_asyncio
import pytest
from httpx import ASGITransport, AsyncClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ["DEBUG"] = "false"

from app.dependencies.profiles import get_profile_manager # noqa E402 
from main import create_app # noqa E402 


@pytest.fixture
def app():
    return create_app()


@pytest_asyncio.fixture
async def client(app) -> Generator[AsyncClient, None, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as test_client:
        yield test_client


@pytest.fixture
def override_manager(app):
    def _override(manager):
        async def _get_manager():
            return manager

        app.dependency_overrides[get_profile_manager] = _get_manager
        return manager

    yield _override
    app.dependency_overrides.clear()
