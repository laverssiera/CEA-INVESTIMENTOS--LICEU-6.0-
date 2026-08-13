from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.automation_storage import append_document, fetch_documents

DOCUMENT_LOG: list[dict[str, Any]] = []


def generate_document(doc_type: str, context: dict[str, Any]) -> dict[str, Any]:
    document = {
        "id": f"DOC-{len(DOCUMENT_LOG) + 1:05d}",
        "type": doc_type,
        "context": context,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "generated",
    }
    DOCUMENT_LOG.append(document)
    append_document(document)
    return document


def generate_investment_contract(investor: str, amount: float) -> dict[str, Any]:
    return generate_document("contrato_investimento", {"investor": investor, "amount": amount})


def generate_financing_term(client: str, amount: float) -> dict[str, Any]:
    return generate_document("termo_financiamento", {"client": client, "amount": amount})


def generate_committee_minutes(committee: str, decision: str) -> dict[str, Any]:
    return generate_document("ata_comite", {"committee": committee, "decision": decision})


def latest_documents(limit: int = 100) -> list[dict[str, Any]]:
    stored = fetch_documents(limit)
    return stored if stored else DOCUMENT_LOG[-limit:]
