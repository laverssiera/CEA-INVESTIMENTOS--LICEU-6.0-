from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.cea.core.database import get_db
from apps.cea.models.wallet import WalletModel
from apps.cea.modules.wallet.service import transfer

router = APIRouter(prefix="/wallet", tags=["Wallet"])


class WalletTransferInput(BaseModel):
    from_id: str
    to_id: str
    amount: float = Field(gt=0)


class WalletCreateInput(BaseModel):
    owner: str
    balance: float = Field(ge=0, default=0)


@router.post("/transfer")
def wallet_transfer(payload: WalletTransferInput, db: Session = Depends(get_db)) -> dict:
    try:
        result = transfer(db, payload.from_id, payload.to_id, payload.amount)
        return {"status": "ok", **result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/create")
def wallet_create(payload: WalletCreateInput, db: Session = Depends(get_db)) -> dict:
    wallet = WalletModel(owner=payload.owner, balance=payload.balance)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return {"id": wallet.id, "owner": wallet.owner, "balance": float(wallet.balance)}


@router.get("/")
def list_wallets(db: Session = Depends(get_db)) -> dict:
    items = db.scalars(select(WalletModel)).all()
    return {
        "items": [
            {"id": item.id, "owner": item.owner, "balance": float(item.balance)}
            for item in items
        ]
    }
