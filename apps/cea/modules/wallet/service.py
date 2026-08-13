from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.cea.models.wallet import WalletModel


def transfer(db: Session, from_id: str, to_id: str, amount: float) -> dict:
    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    from_wallet = db.scalar(select(WalletModel).where(WalletModel.id == from_id))
    to_wallet = db.scalar(select(WalletModel).where(WalletModel.id == to_id))

    if from_wallet is None or to_wallet is None:
        raise ValueError("wallet not found")

    if float(from_wallet.balance) < amount:
        raise ValueError("insufficient funds")

    from_wallet.balance = float(from_wallet.balance) - amount
    to_wallet.balance = float(to_wallet.balance) + amount
    db.commit()

    return {
        "from_wallet": from_id,
        "to_wallet": to_id,
        "amount": amount,
        "from_balance": float(from_wallet.balance),
        "to_balance": float(to_wallet.balance),
    }
