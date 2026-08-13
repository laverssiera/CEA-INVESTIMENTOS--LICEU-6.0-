from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import InvestmentAsset, InvestmentOrder, InvestmentPosition


class InvestmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_assets(self) -> list[InvestmentAsset]:
        return list(self.db.scalars(select(InvestmentAsset).order_by(InvestmentAsset.id)).all())

    def get_asset(self, asset_id: int) -> InvestmentAsset | None:
        return self.db.scalar(select(InvestmentAsset).where(InvestmentAsset.id == asset_id))

    def create_order(self, user_id: int, asset_id: int, amount: float, order_type: str = "buy") -> InvestmentOrder:
        order = InvestmentOrder(user_id=user_id, asset_id=asset_id, amount=amount, order_type=order_type)
        self.db.add(order)
        self.db.flush()
        return order

    def upsert_position(self, user_id: int, asset_id: int, amount_delta: float, expected_yield: float) -> InvestmentPosition:
        position = self.db.scalar(
            select(InvestmentPosition).where(
                InvestmentPosition.user_id == user_id,
                InvestmentPosition.asset_id == asset_id,
            )
        )
        if not position:
            position = InvestmentPosition(
                user_id=user_id,
                asset_id=asset_id,
                invested_amount=0,
                expected_yield=expected_yield,
            )
            self.db.add(position)

        position.invested_amount = float(position.invested_amount) + amount_delta
        position.expected_yield = expected_yield
        self.db.flush()
        return position

    def list_positions(self, user_id: int) -> list[InvestmentPosition]:
        return list(self.db.scalars(select(InvestmentPosition).where(InvestmentPosition.user_id == user_id)).all())

    def list_orders_by_user(self, user_id: int) -> list[InvestmentOrder]:
        return list(
            self.db.scalars(
                select(InvestmentOrder).where(InvestmentOrder.user_id == user_id).order_by(InvestmentOrder.id.desc())
            ).all()
        )
