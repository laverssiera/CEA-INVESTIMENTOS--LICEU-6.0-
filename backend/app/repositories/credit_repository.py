from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CreditRequest


class CreditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_request(self, **kwargs) -> CreditRequest:
        item = CreditRequest(**kwargs)
        self.db.add(item)
        self.db.flush()
        return item

    def list_requests(self) -> list[CreditRequest]:
        return list(self.db.scalars(select(CreditRequest).order_by(CreditRequest.id.desc())).all())
