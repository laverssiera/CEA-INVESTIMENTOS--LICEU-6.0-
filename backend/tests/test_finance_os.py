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


def test_wallet_seed_and_transfer() -> None:
    wallets = client.get("/wallets")
    assert wallets.status_code == 200
    items = wallets.json().get("items", [])
    assert len(items) >= 4

    transfer = client.post(
        "/wallet/transfer",
        json={
            "from_wallet": "CEA_MASTER",
            "to_wallet": "ARCHIMEDES_OPER",
            "amount": 10000,
            "entity_id": "archimedes.project_123",
            "reference": "capital-allocation",
        },
        headers={"x-finance-role": "cfo", "x-finance-user": "u-cfo"},
    )
    assert transfer.status_code == 200
    body = transfer.json()
    assert body.get("amount") == 10000
    assert body.get("ledger_entry_id")


def test_finance_roi_invest_and_cashflow() -> None:
    roi = client.get(
        "/finance/roi/project_123",
        params={"investment_amount": 100000, "current_value": 135000, "discount_rate": 0.01},
    )
    assert roi.status_code == 200
    assert "roi" in roi.json()
    assert "irr" in roi.json()

    invest = client.post(
        "/finance/invest",
        json={
            "source_wallet": "CEA_MASTER",
            "target_wallet": "ARCHIMEDES_OPER",
            "amount": 25000,
            "target": "archimedes.project_123",
            "expected_return": 0.24,
            "risk_score": 0.35,
            "liquidity_score": 0.7,
            "time_horizon_months": 18,
        },
        headers={"x-finance-role": "gestor", "x-finance-user": "u-gestor"},
    )
    assert invest.status_code == 200
    assert invest.json().get("action") in {"invest", "hold"}

    cashflow = client.get("/finance/cashflow", params={"period": "daily"})
    assert cashflow.status_code == 200
    assert "forecast" in cashflow.json()


def test_finance_phase2_endpoints() -> None:
    feed = client.post(
        "/finance/cefeida/feed",
        json={
            "market_trend": "growth",
            "demand_index": 0.8,
            "risk_outlook": 0.3,
            "forecast_confidence": 0.77,
        },
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert feed.status_code == 200
    assert feed.json().get("status") == "ingested"

    john = client.post(
        "/finance/john/decision",
        json={
            "target": "archimedes.project_789",
            "amount": 500000,
            "expected_return": 0.31,
            "risk_score": 0.28,
            "liquidity_score": 0.66,
            "time_horizon_months": 24,
        },
        headers={"x-finance-role": "gestor", "x-finance-user": "u-gestor"},
    )
    assert john.status_code == 200
    assert john.json().get("action") in {"invest", "hold"}
    assert "confidence" in john.json()

    learning = client.post(
        "/finance/learning/feedback",
        json={"target": "archimedes.project_789", "invested_amount": 100000, "realized_return": 16000},
        headers={"x-finance-role": "cfo", "x-finance-user": "u-cfo"},
    )
    assert learning.status_code == 200
    assert learning.json().get("status") == "updated"

    compliance = client.post(
        "/finance/compliance/check",
        json={"contract_valid": True, "legal_risk_score": 0.35, "blocked_by_legal": False},
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert compliance.status_code == 200
    assert compliance.json().get("approved") is True

    antifraud = client.post(
        "/finance/antifraud/check",
        json={
            "transaction_amount": 45000,
            "expected_budget": 50000,
            "velocity_24h": 2,
            "counterpart_mismatch": False,
        },
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert antifraud.status_code == 200
    assert "fraud_score" in antifraud.json()

    output = client.post(
        "/finance/intelligence/output",
        json={
            "entity_id": "archimedes.project_789",
            "roi": 0.22,
            "risk_score": 0.33,
            "liquidity_alert": False,
            "compliance_blocked": False,
        },
    )
    assert output.status_code == 200
    assert output.json().get("recomendacao_investimento") in {"invest", "hold", "blocked"}


def test_finance_phase3_accounting_and_budget() -> None:
    accounting = client.post(
        "/finance/accounting/register",
        json={
            "entity_id": "archimedes",
            "entry_type": "accounts_receivable",
            "amount": 250000,
            "tax_amount": 10000,
            "reference": "sale-001",
        },
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert accounting.status_code == 200
    assert accounting.json().get("entry_type") == "accounts_receivable"

    report = client.get("/finance/accounting/report", params={"entity_id": "archimedes"})
    assert report.status_code == 200
    assert report.json().get("accounts_receivable", 0) >= 250000

    sync = client.post(
        "/finance/accounting/sync-hub",
        params={"entity_id": "archimedes"},
        headers={"x-finance-role": "gestor", "x-finance-user": "u-gestor"},
    )
    assert sync.status_code == 200
    assert sync.json().get("destination") == "hubbackoffice"

    budget_set = client.post(
        "/finance/budget/set",
        json={"entity_id": "archimedes", "period": "2026-04", "planned_amount": 500000},
        headers={"x-finance-role": "cfo", "x-finance-user": "u-cfo"},
    )
    assert budget_set.status_code == 200
    assert budget_set.json().get("planned_amount") == 500000

    budget_exec = client.post(
        "/finance/budget/execute",
        json={
            "entity_id": "archimedes",
            "period": "2026-04",
            "realized_delta": 120000,
            "reason": "marketing and operations",
        },
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert budget_exec.status_code == 200
    assert budget_exec.json().get("realized_amount", 0) >= 120000

    budget_status = client.get("/finance/budget/status", params={"entity_id": "archimedes", "period": "2026-04"})
    assert budget_status.status_code == 200
    assert budget_status.json().get("planned_amount") == 500000


def test_finance_phase4_command_center_liceu_autoinvest_rebalancer() -> None:
    from app.services.automation_storage import append_event, record_event_dispatch
    from uuid import uuid4

    # seed wallets, budget, accounting (re-uses shared DB state from previous tests)
    client.post(
        "/finance/budget/set",
        json={"entity_id": "gamemkt", "period": "2026-04", "planned_amount": 200000},
        headers={"x-finance-role": "cfo", "x-finance-user": "u-cfo"},
    )
    client.post(
        "/finance/budget/execute",
        json={"entity_id": "gamemkt", "period": "2026-04", "realized_delta": 240000, "reason": "overpaid campaign"},
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )

    # Issue 15: Command Center
    cc = client.get("/finance/command-center")
    assert cc.status_code == 200
    body = cc.json()
    assert "total_balance" in body
    assert "wallets" in body
    assert "cefeida_signal" in body
    assert "budget_controls" in body
    assert len(body["wallets"]) >= 4

    # Issue 16: Telão LICEU sync
    liceu = client.post(
        "/finance/liceu/sync",
        headers={"x-finance-role": "cfo", "x-finance-user": "u-cfo"},
    )
    assert liceu.status_code == 200
    assert liceu.json().get("event") == "liceu.finance_snapshot"

    # Sinal favorável para forçar caminho de execução no auto-invest
    feed = client.post(
        "/finance/cefeida/feed",
        json={
            "market_trend": "growth",
            "demand_index": 1.0,
            "risk_outlook": 0.0,
            "forecast_confidence": 1.0,
        },
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert feed.status_code == 200

    # Issue 19: Auto Invest Engine — action must be invest or blocked
    auto = client.post(
        "/finance/auto-invest/trigger",
        json={
            "source_wallet": "CEA_MASTER",
            "target_wallet": "ARCHIMEDES_OPER",
            "amount": 15000,
            "target": "archimedes.auto_project",
            "expected_return": 0.9,
            "risk_score": 0.05,
            "liquidity_score": 1.0,
            "time_horizon_months": 1,
        },
        headers={"x-finance-role": "cfo", "x-finance-user": "u-cfo"},
    )
    assert auto.status_code == 200
    assert auto.json().get("action") in {"invest", "hold", "blocked"}
    assert "compliance" in auto.json()
    assert "antifraud" in auto.json()
    assert auto.json().get("executed") is True
    assert auto.json().get("transfer")

    audit = client.get(
        "/finance/audit",
        params={"action": "finance.auto_invest_trigger", "limit": 20},
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert audit.status_code == 200
    assert audit.json().get("count", 0) >= 1

    dispatches = client.get(
        "/finance/events/dispatches",
        params={"transport": "nats", "limit": 20},
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert dispatches.status_code == 200
    assert "summary" in dispatches.json()
    assert "items" in dispatches.json()

    failed_event_id = f"EVT-{uuid4().hex}"
    append_event("archimedes.deal_created", {"deal": "D-001"}, event_id=failed_event_id)
    record_event_dispatch(
        event_id=failed_event_id,
        transport="nats",
        status="failed",
        error="integration_test",
    )

    metrics = client.get(
        "/finance/events/dispatches/metrics",
        params={"window_hours": 24, "transport": "nats"},
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert metrics.status_code == 200
    assert metrics.json().get("window_hours") == 24
    assert "failure_rate" in metrics.json()

    top_failures = client.get(
        "/finance/events/dispatches/top-failures",
        params={"window_hours": 24, "transport": "nats", "limit": 5, "group_by": "event_error"},
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert top_failures.status_code == 200
    assert "top_failures" in top_failures.json()
    assert top_failures.json().get("window_hours") == 24
    assert top_failures.json().get("transport") == "nats"
    assert top_failures.json().get("group_by") == "event_error"

    top_failures_by_event = client.get(
        "/finance/events/dispatches/top-failures",
        params={"window_hours": 24, "transport": "nats", "limit": 5, "group_by": "event_name"},
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert top_failures_by_event.status_code == 200
    assert top_failures_by_event.json().get("group_by") == "event_name"
    assert "top_failures" in top_failures_by_event.json()

    reprocess = client.post(
        "/finance/events/dispatches/reprocess",
        json={"event_id": failed_event_id, "transport": "nats"},
        headers={"x-finance-role": "cfo", "x-finance-user": "u-cfo"},
    )
    assert reprocess.status_code == 200
    assert reprocess.json().get("event_id") == failed_event_id
    assert reprocess.json().get("result", {}).get("status") in {
        "reprocessed",
        "failed",
        "skipped",
        "not_found",
        "event_payload_not_found",
        "skipped_not_failed",
        "unsupported_transport",
    }

    # Issue 20: Budget Rebalancer
    rebalance = client.get("/finance/budget/rebalance", params={"period": "2026-04"})
    assert rebalance.status_code == 200
    rb = rebalance.json()
    assert "surplus_pool" in rb
    assert "proposals" in rb
    assert "rebalance_feasible" in rb


def test_finance_phase5_sla_and_kanban() -> None:
    from datetime import datetime, timedelta, timezone

    deadline = (datetime.now(timezone.utc) + timedelta(hours=4)).isoformat()
    future = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    # --- SLA ---
    sla_create = client.post(
        "/finance/sla/create",
        json={
            "entity_id": "hubbackoffice",
            "task_type": "payment",
            "priority": "high",
            "sla_deadline": deadline,
            "metadata": {"invoice_ref": "INV-2026-001"},
        },
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert sla_create.status_code == 200
    task = sla_create.json()
    assert task["task_type"] == "payment"
    assert task["status"] == "pending"
    task_id = task["id"]

    # Update to in_progress
    sla_update = client.post(
        "/finance/sla/update",
        json={"task_id": task_id, "new_status": "in_progress"},
        headers={"x-finance-role": "gestor", "x-finance-user": "u-gestor"},
    )
    assert sla_update.status_code == 200
    assert sla_update.json()["status"] == "in_progress"

    # Complete the task
    sla_done = client.post(
        "/finance/sla/update",
        json={"task_id": task_id, "new_status": "completed"},
        headers={"x-finance-role": "gestor", "x-finance-user": "u-gestor"},
    )
    assert sla_done.status_code == 200
    assert sla_done.json()["completed_at"] is not None

    # List SLA tasks
    sla_list = client.get("/finance/sla/list", params={"entity_id": "hubbackoffice"})
    assert sla_list.status_code == 200
    assert sla_list.json()["count"] >= 1

    # --- Kanban ---
    card_create = client.post(
        "/finance/kanban/create",
        json={
            "entity_id": "hubbackoffice",
            "title": "Processar fatura INV-2026-001",
            "description": "Pagamento de fornecedor urgente",
            "board": "finance",
            "column": "backlog",
            "priority": "high",
            "linked_sla_id": task_id,
            "linked_entity_type": "sla_task",
            "due_date": future,
        },
        headers={"x-finance-role": "analista", "x-finance-user": "u-analista"},
    )
    assert card_create.status_code == 200
    card = card_create.json()
    assert card["board"] == "finance"
    assert card["column"] == "backlog"
    card_id = card["id"]

    # Move card
    move = client.post(
        "/finance/kanban/move",
        json={"card_id": card_id, "new_column": "in_progress"},
        headers={"x-finance-role": "gestor", "x-finance-user": "u-gestor"},
    )
    assert move.status_code == 200
    assert move.json()["column"] == "in_progress"

    # Board view
    board = client.get("/finance/kanban/board", params={"board": "finance"})
    assert board.status_code == 200
    assert "columns" in board.json()
    assert "in_progress" in board.json()["columns"]

    # List cards
    cards_list = client.get("/finance/kanban/list", params={"board": "finance"})
    assert cards_list.status_code == 200
    assert cards_list.json()["count"] >= 1
