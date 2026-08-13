from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from app.datawarehouse.schemas import DW_TABLES


def _append_metric(table_name: str, data: dict[str, Any]) -> dict[str, Any]:
    row = {
        "id": f"{table_name}-{len(DW_TABLES[table_name]) + 1}",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        **data,
    }
    DW_TABLES[table_name].append(row)
    return row


def etl_daily_metrics() -> dict[str, Any]:
    today = date.today().isoformat()
    _append_metric("dw_investor_metrics", {"ref_date": today, "active_investors": 128, "new_investments": 14})
    _append_metric("dw_project_metrics", {"ref_date": today, "active_projects": 7, "avg_progress": 58.3})
    _append_metric("dw_risk_metrics", {"ref_date": today, "portfolio_var": 0.021, "concentration": 24.5})
    _append_metric("dw_credit_metrics", {"ref_date": today, "approved": 6, "pending": 11})
    _append_metric("dw_treasury_metrics", {"ref_date": today, "cash_balance": 48200000, "liquidity_gap": 0.07})
    _append_metric("dw_esg_metrics", {"ref_date": today, "esg_score": 79, "pending_actions": 4})
    return {"status": "ok", "job": "etl_daily_metrics"}


def etl_weekly_performance() -> dict[str, Any]:
    _append_metric("dw_investor_metrics", {"period": "weekly", "yield_avg": 0.0118, "retention": 0.97})
    _append_metric("dw_project_metrics", {"period": "weekly", "throughput": 0.91, "on_time": 0.86})
    return {"status": "ok", "job": "etl_weekly_performance"}


def etl_risk_history() -> dict[str, Any]:
    _append_metric("dw_risk_metrics", {"period": "history", "stress_events": 2, "risk_alerts": 5})
    return {"status": "ok", "job": "etl_risk_history"}
