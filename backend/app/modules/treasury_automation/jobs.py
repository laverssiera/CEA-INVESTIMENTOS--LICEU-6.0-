from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TREASURY_AUTOMATION_LOG: list[dict[str, Any]] = []


def _log(job_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = {
        "job": job_name,
        "payload": payload,
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }
    TREASURY_AUTOMATION_LOG.append(row)
    return row


def treasury_cashflow_projection() -> dict[str, Any]:
    return _log("treasury_cashflow_projection", {"d1": 4_200_000, "d7": 18_500_000, "d30": 62_000_000})


def liquidity_gap_analysis() -> dict[str, Any]:
    return _log("liquidity_gap_analysis", {"gap_pct": 0.06, "status": "attention"})


def funding_allocation() -> dict[str, Any]:
    return _log("funding_allocation", {"allocated_to_credit": 12_500_000, "remaining_liquidity": 37_400_000})


def daily_treasury_report() -> dict[str, Any]:
    return _log("daily_treasury_report", {"dre_operacional": 1_240_000, "conciliation": "ok"})
