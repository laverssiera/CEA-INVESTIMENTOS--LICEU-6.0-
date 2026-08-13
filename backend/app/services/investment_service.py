from sqlalchemy.orm import Session

from app.repositories.investment_repository import InvestmentRepository


class InvestmentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = InvestmentRepository(db)

    def place_order(self, user_id: int, asset_id: int, amount: float):
        asset = self.repo.get_asset(asset_id)
        if not asset:
            raise ValueError("Asset not found")

        order = self.repo.create_order(user_id=user_id, asset_id=asset_id, amount=amount)
        self.repo.upsert_position(user_id=user_id, asset_id=asset_id, amount_delta=amount, expected_yield=float(asset.yield_value))
        self.db.commit()
        return order
