from __future__ import annotations

from sqlalchemy.orm import Session

from apps.cea.models.ledger import LedgerModel


def create_entry(
    db: Session,
    entity_id: str,
    debit_account: str,
    credit_account: str,
    amount: float,
) -> LedgerModel:
    entry = LedgerModel(
        entity_id=entity_id,
        debit_account=debit_account,
        credit_account=credit_account,
        amount=amount,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
