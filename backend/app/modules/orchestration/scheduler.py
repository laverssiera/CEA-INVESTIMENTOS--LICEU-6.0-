from __future__ import annotations

import os
from typing import Any

from app.events import event_bus
from app.modules.orchestration.orchestrator import Orchestrator

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
except Exception:  # pragma: no cover
    AsyncIOScheduler = None
    CronTrigger = None


class OrchestrationScheduler:
    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
        self.enabled = os.getenv("CEA_ORCHESTRATION_ENABLED", "1") == "1"
        self.use_apscheduler = os.getenv("CEA_ORCHESTRATION_SCHEDULER", "apscheduler") == "apscheduler"
        self.scheduler = AsyncIOScheduler(timezone="UTC") if AsyncIOScheduler and self.enabled and self.use_apscheduler else None

    def start(self) -> dict[str, Any]:
        if not self.enabled:
            return {"status": "disabled", "reason": "CEA_ORCHESTRATION_ENABLED=0"}

        if self.scheduler is None:
            return {
                "status": "fallback",
                "scheduler": "cron",
                "message": "APScheduler indisponivel. Use backend/docker/cron/orchestration.cron no container.",
            }

        self._register_jobs()
        if not self.scheduler.running:
            self.scheduler.start()

        return {"status": "running", "scheduler": "apscheduler"}

    def shutdown(self) -> None:
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    def _safe_run(self, job_name: str) -> None:
        result = self.orchestrator.run_job(job_name)
        if job_name in {"daily_yield_calculation", "daily_risk_consolidation", "liceu_project_sync"}:
            event_bus.publish("daily.close", {"source": job_name})
        if job_name == "liceu_project_sync":
            event_bus.publish("project.updated", {"source": "scheduler"})
        if job_name == "daily_risk_consolidation":
            event_bus.publish("risk.alert", {"source": "scheduler", "result": result["result"]})

    def _register_jobs(self) -> None:
        jobs = [
            ("daily_risk_consolidation", "10 1 * * *"),
            ("daily_yield_calculation", "20 1 * * *"),
            ("credit_score_refresh", "30 1 * * *"),
            ("liceu_project_sync", "40 1 * * *"),
            ("liquidity_check", "50 1 * * *"),
            ("investor_notifications", "0 2 * * *"),
            ("esg_score_update", "30 2 * * *"),
            ("audit_snapshot", "0 3 * * *"),
        ]
        for name, cron in jobs:
            minute, hour, day, month, dow = cron.split(" ")
            self.scheduler.add_job(
                self._safe_run,
                trigger=CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=dow),
                args=[name],
                id=f"auto_{name}",
                replace_existing=True,
            )
