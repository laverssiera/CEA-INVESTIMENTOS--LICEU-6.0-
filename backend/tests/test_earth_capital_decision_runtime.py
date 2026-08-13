from __future__ import annotations

from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.runtime.investments import EarthInvestmentRuntime, EarthPortfolioRuntime, EarthProjectScoreRuntime


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


def test_earth_investment_runtime_returns_full_capital_metrics() -> None:
    runtime = EarthInvestmentRuntime()

    result = runtime.evaluate_project(
        project_name="Nova ferrovia",
        project_type="ferrovia",
        location="Corredor logistico nacional",
        capex=100_000_000,
        opex_yearly=5_000_000,
        annual_revenue=18_000_000,
        discount_rate=0.08,
        horizon_years=10,
    )

    assert result["project_name"] == "Nova ferrovia"
    assert result["capex"] == 100_000_000
    assert result["opex"] == 5_000_000
    assert result["cash_flow"][0] == -100_000_000.0
    assert "npv" in result
    assert "irr" in result
    assert "payback" in result
    assert "roi" in result
    assert "impacto_estrategico" in result
    assert result["risk"]["score"] >= 0.0
    assert result["impacto_estrategico"]["score"] >= 0.0


def test_earth_project_score_ranks_projects_for_capital_allocation() -> None:
    runtime = EarthProjectScoreRuntime()

    result = runtime.score_projects(
        [
            {
                "project_name": "Nova ferrovia",
                "project_type": "ferrovia",
                "location": "Centro-oeste",
                "budget": 120_000_000,
            },
            {
                "project_name": "Usina solar",
                "project_type": "usina solar",
                "location": "Nordeste",
                "budget": 80_000_000,
            },
            {
                "project_name": "Data center",
                "project_type": "data center",
                "location": "Sudeste",
                "budget": 60_000_000,
            },
        ]
    )

    assert result["status"] == "scored"
    assert result["total_projects"] == 3
    assert result["recommended_project"] is not None
    assert [project["rank"] for project in result["projects"]] == [1, 2, 3]
    assert all("decision_score" in project for project in result["projects"])


def test_earth_portfolio_builds_capital_decision_with_budget() -> None:
    runtime = EarthPortfolioRuntime()

    result = runtime.build_portfolio(
        [
            {
                "project_name": "Nova ferrovia",
                "project_type": "ferrovia",
                "location": "Corredor 1",
                "budget": 120_000_000,
            },
            {
                "project_name": "Hospital regional",
                "project_type": "hospital",
                "location": "Regiao 2",
                "budget": 70_000_000,
            },
            {
                "project_name": "Sistema hidrico",
                "project_type": "sistema hidrico",
                "location": "Bacia 3",
                "budget": 90_000_000,
            },
        ],
        available_capital=190_000_000,
    )

    assert result["status"] == "portfolio_built"
    assert result["allocated_capital"] <= 190_000_000
    assert result["selected_projects"]
    assert "portfolio_npv" in result
    assert result["financial_exposure"] >= result["allocated_capital"]
    assert "portfolio_strategic_impact" in result


def test_earth_project_score_api_endpoint_returns_full_analysis() -> None:
    response = client.post(
        "/investments/earth/project/score",
        json={
            "name": "Porto de exportacao",
            "location": "Litoral sul",
            "complexity": 8,
            "budget": 150000000,
            "project_type": "porto",
            "capex": 150000000,
            "opex_yearly": 7500000,
            "annual_revenue": 28500000,
            "physical_event": {
                "event_type": "flood",
                "severity": 0.7,
                "probability": 0.4,
                "affected_asset_value": 10000000,
                "repair_cost": 2000000,
                "annual_revenue_at_risk": 1000000,
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] in {"fund", "review", "defer"}
    assert body["risk"]["score"] >= 0.0
    assert body["impacto_estrategico"]["score"] >= 0.0
    assert body["economic_impact"]["status"] == "assessed"
    assert body["financial_exposure"] > body["capex"]


def test_earth_project_examples_endpoint_returns_catalog() -> None:
    response = client.get("/investments/earth/projects/examples")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "examples_ready"
    assert body["count"] == 6
    assert body["recommended_project"] is not None
    assert {project["project_name"] for project in body["projects"]} >= {
        "Nova ferrovia",
        "Usina solar",
        "Porto",
        "Hospital",
        "Data center",
        "Sistema hídrico",
    }