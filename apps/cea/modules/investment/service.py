from __future__ import annotations

import json

from sqlalchemy.orm import Session

from apps.cea.core.nats import connect_nats
from apps.cea.models.investment import InvestmentModel
from apps.cea.modules.ledger.service import create_entry


async def evaluate_event(db: Session, subject: str, data: dict) -> InvestmentModel:
    value = float(data.get("value", 0))
    entity_id = str(data.get("entity_id", "unknown"))

    expected_roi = 0.18 if value > 100000 else 0.10

    investment = InvestmentModel(
        entity_id=entity_id,
        amount=value,
        expected_roi=expected_roi,
        status="approved",
    )
    db.add(investment)
    db.commit()
    db.refresh(investment)

    create_entry(
        db=db,
        entity_id=entity_id,
        debit_account=f"investment:{subject}",
        credit_account="wallet:CEA_MASTER",
        amount=value,
    )

    nc = await connect_nats()
    await nc.publish(
        "john.finance.decision",
        json.dumps(
            {
                "entity_id": entity_id,
                "action": "invest",
                "amount": value,
                "roi": expected_roi,
                "source_event": subject,
            }
        ).encode(),
    )

    return investment


def create_manual_investment(db: Session, entity_id: str, amount: float, expected_roi: float) -> InvestmentModel:
    investment = InvestmentModel(
        entity_id=entity_id,
        amount=amount,
        expected_roi=expected_roi,
        status="approved",
    )
    db.add(investment)
    db.commit()
    db.refresh(investment)
    return investment
