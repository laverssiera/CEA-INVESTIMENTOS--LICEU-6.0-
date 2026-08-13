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


def test_civilization_portfolio_alias_endpoints() -> None:
    create = client.post(
        "/investments/civilization/portfolio/create",
        json={
            "owner_id": "civilization-owner-1",
            "region": "Orbital",
            "assets": [
                {"asset_id": "CIV-001", "value": 125000},
                {"asset_id": "CIV-002", "value": 75000},
            ],
        },
    )
    assert create.status_code == 200
    created = create.json()
    assert created["status"] == "active"
    assert created["total_initial_value"] == 200000.0

    state = client.get("/investments/civilization/portfolio/state")
    assert state.status_code == 200
    state_body = state.json()
    assert state_body["status"] == "operational"
    assert state_body["regions"]["Orbital"] >= 1

    portfolio = client.get(f"/investments/civilization/portfolio/{created['portfolio_id']}")
    assert portfolio.status_code == 200
    portfolio_body = portfolio.json()
    assert portfolio_body["owner_id"] == "civilization-owner-1"


def test_civilization_risk_capital_and_investment_alias_endpoints() -> None:
    risk = client.post(
        "/investments/civilization/risk/score",
        json={
            "name": "Base Marciana",
            "location": "Base Marciana Alpha",
            "complexity": 7,
            "budget": 3000000,
        },
    )
    assert risk.status_code == 200
    risk_body = risk.json()
    assert "score" in risk_body
    assert risk_body["classification"] in {"Low", "Medium", "High"}

    capital = client.post(
        "/investments/civilization/capital/suggest",
        params={"total_capital": 500000, "risk_profile": "Moderate"},
    )
    assert capital.status_code == 200
    capital_body = capital.json()
    assert capital_body["risk_profile"] == "Moderate"
    assert len(capital_body["allocations"]) == 3

    project_finance = client.post(
        "/investments/civilization/project/finance",
        json=[-500000, 150000, 180000, 250000],
        params={"discount_rate": 0.1},
    )
    assert project_finance.status_code == 200
    project_finance_body = project_finance.json()
    assert "npv" in project_finance_body
    assert "irr" in project_finance_body

    investment = client.post(
        "/investments/civilization/investment/analyze",
        params={"region": "Mars", "investment_type": "Infrastructure", "amount": 750000},
    )
    assert investment.status_code == 200
    investment_body = investment.json()
    assert investment_body["region"] == "Mars"
    assert investment_body["recommended"] is True