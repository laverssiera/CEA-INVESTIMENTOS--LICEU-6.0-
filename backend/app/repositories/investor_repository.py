from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Investor


class InvestorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> Investor | None:
        return self.db.scalar(select(Investor).where(Investor.user_id == user_id))

    def create(self, user_id: int, profile_type: str) -> Investor:
        investor = Investor(user_id=user_id, profile_type=profile_type)
        self.db.add(investor)
        self.db.flush()
        return investor

    def update_kyc(self, investor: Investor, payload: dict) -> Investor:
        investor.cpf_cnpj = payload.get("cpf")
        investor.address = payload.get("address")
        investor.income_brl = payload.get("income_brl", investor.income_brl)
        investor.patrimony_brl = payload.get("patrimony_brl", investor.patrimony_brl)
        investor.source_of_funds = payload.get("origin_of_funds")
        investor.kyc_status = "pending"
        self.db.flush()
        return investor
