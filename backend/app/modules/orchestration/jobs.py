from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from app.datawarehouse import etl_daily_metrics, etl_risk_history, etl_weekly_performance
from app.events import event_bus
from app.modules.compliance_engine import aml_screening, audit_log_snapshot, kyc_pending_check, suitability_revalidation
from app.modules.decision_engine import process_trigger
from app.modules.documents.service import generate_committee_minutes, generate_document
from app.modules.notifications import send_notification
from app.modules.treasury_automation import (
    daily_treasury_report,
    funding_allocation,
    liquidity_gap_analysis,
    treasury_cashflow_projection,
)
from app.services.automation_storage import append_job_run

JOB_LOG: list[dict[str, Any]] = []


def _track(job_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = {
        "job": job_name,
        "payload": payload,
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }
    JOB_LOG.append(row)
    append_job_run(job_name, payload)
    return row


def daily_risk_consolidation() -> dict[str, Any]:
    result = _track("daily_risk_consolidation", {"risk_score": 41.2, "concentration": 24.5})
    event_bus.publish("risk.alert", {"level": "medium", "source": "daily_risk_consolidation"})
    return result


def daily_yield_calculation() -> dict[str, Any]:
    return _track("daily_yield_calculation", {"average_yield": 0.0118, "updated_positions": 148})


def credit_score_refresh() -> dict[str, Any]:
    score = process_trigger("daily.close", {"score": 710, "ltv": 0.66, "risk_flag": False})
    return _track("credit_score_refresh", {"decision": score})


def liceu_project_sync() -> dict[str, Any]:
    event_bus.publish("project.updated", {"projects": 7, "source": "liceu_project_sync"})
    return _track("liceu_project_sync", {"projects_synced": 7, "status": "ok"})


def liquidity_check() -> dict[str, Any]:
    treasury_cashflow_projection()
    gap = liquidity_gap_analysis()
    if gap["payload"]["gap_pct"] >= 0.06:
        event_bus.publish("treasury.liquidity_low", {"gap_pct": gap["payload"]["gap_pct"]})
    return _track("liquidity_check", gap["payload"])


def investor_notifications() -> dict[str, Any]:
    sent = [
        send_notification("email", "pagamento_rendimento", "investidor@demo.com", "Rendimento diario processado."),
        send_notification("dashboard", "risco_elevado", "admin", "Risco elevado detectado em 1 carteira."),
    ]
    return _track("investor_notifications", {"messages": len(sent)})


def esg_score_update() -> dict[str, Any]:
    etl_weekly_performance()
    return _track("esg_score_update", {"new_score": 80, "pending_actions": 3})


def audit_snapshot() -> dict[str, Any]:
    audit_log_snapshot()
    generate_committee_minutes("Comite de Risco", "Snapshot de auditoria registrado")
    return _track("audit_snapshot", {"audit_entries": 320, "integrity": "ok"})


def treasury_projection() -> dict[str, Any]:
    projection = treasury_cashflow_projection()
    funding_allocation()
    daily_treasury_report()
    return _track("treasury_projection", projection["payload"])


def ml_rebalance() -> dict[str, Any]:
    decision = process_trigger("market.updated", {"exposure_by_asset": {"debentures": 55, "caixa": 20, "fundo_di": 25}})
    return _track("ml_rebalance", decision)


def dw_metrics() -> dict[str, Any]:
    etl_daily_metrics()
    etl_risk_history()
    return _track("dw_metrics", {"tables": 6, "status": "updated"})


def autopilot_pipeline() -> dict[str, Any]:
    kyc = kyc_pending_check()
    aml = aml_screening()
    suitability = suitability_revalidation()
    recommendation = process_trigger("investment.created", {"amount": 150000, "profile": "moderado", "risk": 52})
    contract = generate_document("contrato_investimento", {"investor": "auto", "amount": 150000})
    notification = send_notification("whatsapp", "investimento_aprovado", "+5511999999999", "Investimento aprovado e contrato gerado.")

    return _track(
        "autopilot_pipeline",
        {
            "kyc": kyc["payload"],
            "aml": aml["payload"],
            "suitability": suitability["payload"],
            "recommendation": recommendation,
            "document_id": contract["id"],
            "notification_id": notification["id"],
        },
    )


JOB_HANDLERS: dict[str, Callable[[], dict[str, Any]]] = {
    "daily_risk_consolidation": daily_risk_consolidation,
    "daily_yield_calculation": daily_yield_calculation,
    "yield_calculation": daily_yield_calculation,
    "credit_score_refresh": credit_score_refresh,
    "liceu_project_sync": liceu_project_sync,
    "liquidity_check": liquidity_check,
    "investor_notifications": investor_notifications,
    "esg_score_update": esg_score_update,
    "audit_snapshot": audit_snapshot,
    "treasury_cashflow_projection": treasury_cashflow_projection,
    "liquidity_gap_analysis": liquidity_gap_analysis,
    "funding_allocation": funding_allocation,
    "daily_treasury_report": daily_treasury_report,
    "kyc_pending_check": kyc_pending_check,
    "aml_screening": aml_screening,
    "suitability_revalidation": suitability_revalidation,
    "audit_log_snapshot": audit_log_snapshot,
    "etl_daily_metrics": etl_daily_metrics,
    "etl_weekly_performance": etl_weekly_performance,
    "etl_risk_history": etl_risk_history,
    "treasury_projection": treasury_projection,
    "ml_rebalance": ml_rebalance,
    "dw_metrics": dw_metrics,
    "autopilot_pipeline": autopilot_pipeline,
}
