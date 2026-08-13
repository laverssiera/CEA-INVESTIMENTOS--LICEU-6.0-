from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.modules.orchestration.jobs import JOB_HANDLERS


class Orchestrator:
    def __init__(self) -> None:
        self.job_handlers = JOB_HANDLERS

    def list_jobs(self) -> list[str]:
        return sorted(self.job_handlers.keys())

    def run_job(self, job_name: str) -> dict[str, Any]:
        handler = self.job_handlers.get(job_name)
        if not handler:
            raise KeyError(f"Job nao encontrado: {job_name}")

        result = handler()
        return {
            "job": job_name,
            "status": "completed",
            "executed_at": datetime.now(timezone.utc).isoformat(),
            "result": result,
        }


def build_orchestrator() -> Orchestrator:
    return Orchestrator()
