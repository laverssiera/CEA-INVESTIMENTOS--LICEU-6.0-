from sqlalchemy.orm import Session

from app.repositories.credit_repository import CreditRepository


class CreditService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CreditRepository(db)

    def submit_request(self, payload: dict):
        item = self.repo.create_request(**payload)
        self.db.commit()
        return item
