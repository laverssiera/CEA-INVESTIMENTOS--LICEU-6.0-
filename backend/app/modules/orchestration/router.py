from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.modules.orchestration.jobs import JOB_LOG
from app.modules.orchestration.orchestrator import build_orchestrator
from app.services.automation_storage import fetch_events, fetch_job_runs

router = APIRouter(prefix="/api/orchestration", tags=["Orchestration"])
orchestrator = build_orchestrator()

PRIORITY_JOBS = {
    "priority_1": [
        "daily_risk_consolidation",
        "daily_yield_calculation",
        "liceu_project_sync",
        "credit_score_refresh",
    ],
    "priority_2": [
        "treasury_projection",
        "investor_notifications",
        "audit_snapshot",
    ],
    "priority_3": [
        "ml_rebalance",
        "esg_score_update",
        "dw_metrics",
    ],
}


@router.get("/jobs")
def list_jobs() -> dict[str, Any]:
    return {
        "items": orchestrator.list_jobs(),
        "priorities": PRIORITY_JOBS,
    }


@router.post("/run/{job_name}")
def run_job(job_name: str) -> dict[str, Any]:
    try:
        return orchestrator.run_job(job_name)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/logs")
def logs() -> dict[str, Any]:
    items = fetch_job_runs(200)
    return {"items": items if items else JOB_LOG[-200:]}


@router.get("/events")
def events() -> dict[str, Any]:
    return {"items": fetch_events(200)}
