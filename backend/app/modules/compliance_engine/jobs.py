from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

COMPLIANCE_LOG: list[dict[str, Any]] = []


def _log(job_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = {
        "job": job_name,
        "payload": payload,
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }
    COMPLIANCE_LOG.append(row)
    return row


def kyc_pending_check() -> dict[str, Any]:
    return _log("kyc_pending_check", {"pending": 14, "status": "review"})


def aml_screening() -> dict[str, Any]:
    return _log("aml_screening", {"screened": 148, "flags": 2})


def suitability_revalidation() -> dict[str, Any]:
    return _log("suitability_revalidation", {"checked": 86, "outdated": 5})


def audit_log_snapshot() -> dict[str, Any]:
    return _log("audit_log_snapshot", {"entries": 320, "integrity": "ok"})
