from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TreasuryTransaction


class TreasuryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, **kwargs) -> TreasuryTransaction:
        trx = TreasuryTransaction(**kwargs)
        self.db.add(trx)
        self.db.flush()
        return trx

    def list_transactions(self) -> list[TreasuryTransaction]:
        return list(self.db.scalars(select(TreasuryTransaction).order_by(TreasuryTransaction.id.desc())).all())
