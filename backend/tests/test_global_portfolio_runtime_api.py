from __future__ import annotations

from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


TEST_ENGINE = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=TEST_ENGINE, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=TEST_ENGINE)


def _sqlite_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _sqlite_db
client = TestClient(app)


def test_global_portfolio_create_and_get() -> None:
    create = client.post(
        "/investments/portfolio/global/create",
        json={
            "owner_id": "owner-global-1",
            "region": "LatAm",
            "assets": [
                {"asset_id": "AST-001", "value": 100000},
                {"asset_id": "AST-002", "value": 50000},
            ],
        },
    )
    assert create.status_code == 200
    created = create.json()
    assert created["owner_id"] == "owner-global-1"
    assert created["region"] == "LatAm"
    assert created["total_initial_value"] == 150000.0
    assert created["status"] == "active"
    assert "portfolio_id" in created

    state = client.get(f"/investments/portfolio/global/{created['portfolio_id']}")
    assert state.status_code == 200
    body = state.json()
    assert body["portfolio_id"] == created["portfolio_id"]
    assert body["owner_id"] == "owner-global-1"
    assert len(body["assets"]) == 2


def test_global_portfolio_state_and_runtime_metrics() -> None:
    before_state = client.get("/investments/portfolio/global/state")
    assert before_state.status_code == 200
    before = before_state.json()
    before_total = before.get("total_portfolios", 0)

    create = client.post(
        "/investments/portfolio/global/create",
        json={
            "owner_id": "owner-global-2",
            "assets": [
                {"asset_id": "AST-003", "value": 250000},
            ],
        },
    )
    assert create.status_code == 200

    after_state = client.get("/investments/portfolio/global/state")
    assert after_state.status_code == 200
    after = after_state.json()
    assert after["status"] == "operational"
    assert after["total_portfolios"] == before_total + 1
    assert after["total_initial_value"] >= 250000.0
    assert "global" in after["regions"]

    investments_state = client.get("/investments/state")
    assert investments_state.status_code == 200
    metrics = investments_state.json().get("metrics", {})
    active = investments_state.json().get("active_runtimes", [])
    assert "global_portfolio_runtime" in active
    assert metrics.get("total_global_portfolios_managed", 0) >= 1
