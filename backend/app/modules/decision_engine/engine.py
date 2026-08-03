from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.events import event_bus

DECISION_AUDIT: list[dict[str, Any]] = []


def _log(kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = {
        "kind": kind,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    DECISION_AUDIT.append(row)
    return row


def auto_allocation(amount: float, profile: str, risk_level: float) -> dict[str, Any]:
    if profile == "conservador" or risk_level > 70:
        strategy = "preservacao_caixa"
        allocation = {"tesouro_selic": 0.65, "cdb_diario": 0.35}
    elif profile == "arrojado" and risk_level < 45:
        strategy = "crescimento_controlado"
        allocation = {"debentures": 0.5, "fundo_di": 0.2, "tesouro_ipca": 0.3}
    else:
        strategy = "equilibrado"
        allocation = {"cdb_diario": 0.4, "fundo_di": 0.35, "tesouro_ipca": 0.25}

    result = {
        "strategy": strategy,
        "allocation": allocation,
        "recommended_amount": round(amount, 2),
    }
    _log("allocation.auto", result)
    return result


def pre_credit_approval(score: float, ltv: float, risk_flag: bool) -> dict[str, Any]:
    approved = score >= 680 and ltv <= 0.75 and not risk_flag
    reason = "pre_approved" if approved else "manual_review"
    limit = 0 if not approved else round((score - 600) * 2500, 2)

    result = {
        "approved": approved,
        "reason": reason,
        "suggested_limit": limit,
    }
    _log("credit.pre_approval", result)
    return result


def rebalance_portfolio(exposure_by_asset: dict[str, float]) -> dict[str, Any]:
    total = sum(exposure_by_asset.values()) or 1.0
    weights = {key: value / total for key, value in exposure_by_asset.items()}

    alerts = [name for name, weight in weights.items() if weight > 0.5]
    action = "rebalance_required" if alerts else "within_limits"
    result = {
        "action": action,
        "weights": {k: round(v, 4) for k, v in weights.items()},
        "alerts": alerts,
    }
    _log("portfolio.rebalance", result)
    return result


def ml_alerts() -> list[dict[str, Any]]:
    latest = DECISION_AUDIT[-8:]
    alerts: list[dict[str, Any]] = []
    for row in latest:
        if row["kind"] == "portfolio.rebalance" and row["payload"].get("alerts"):
            alerts.append({"type": "exposure", "message": "Concentracao acima de 50% detectada."})
        if row["kind"] == "credit.pre_approval" and not row["payload"].get("approved"):
            alerts.append({"type": "credit", "message": "Pre-credito enviado para revisao manual."})

    return alerts or [{"type": "info", "message": "Motor de decisao operando dentro da normalidade."}]


def process_trigger(trigger: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    if trigger == "investment.created":
        return auto_allocation(payload.get("amount", 10000.0), payload.get("profile", "moderado"), payload.get("risk", 55.0))
    if trigger == "market.updated":
        return rebalance_portfolio(payload.get("exposure_by_asset", {"fundo_di": 38, "debentures": 42, "caixa": 20}))
    if trigger == "daily.close":
        return pre_credit_approval(payload.get("score", 705), payload.get("ltv", 0.68), payload.get("risk_flag", False))

    return {"status": "ignored", "trigger": trigger}


def register_trigger_handlers() -> None:
    event_bus.subscribe("investment.created", lambda event: process_trigger("investment.created", event["payload"]))
    event_bus.subscribe("market.updated", lambda event: process_trigger("market.updated", event["payload"]))
    event_bus.subscribe("daily.close", lambda event: process_trigger("daily.close", event["payload"]))
