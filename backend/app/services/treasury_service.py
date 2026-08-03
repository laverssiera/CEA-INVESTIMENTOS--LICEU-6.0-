from sqlalchemy.orm import Session

from app.repositories.treasury_repository import TreasuryRepository


class TreasuryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TreasuryRepository(db)

    def create_transaction(self, payload: dict):
        trx = self.repo.create_transaction(**payload)
        self.db.commit()
        return trx
