from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from apps.cea.models.ledger import LedgerModel


def get_cashflow(db: Session) -> dict:
    total = db.scalar(select(func.coalesce(func.sum(LedgerModel.amount), 0)))
    return {"cashflow": float(total or 0)}
