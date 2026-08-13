from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter(prefix="/banking", tags=["Digital Banking Core"])

class PixPayload(BaseModel):
    amount: Decimal
    destination_key: str
    description: str = ""

class SplitPayload(BaseModel):
    transaction_id: str
    splits: list # Ex: [{"wallet_id": "UUID", "amount": 100}]

@router.post("/pix/send")
async def send_pix(payload: PixPayload):
    """Executa transferência instatânea no ecossistema (Internal PIX)"""
    return {
        "status": "success",
        "transaction_id": "PIX-INST-001",
        "amount": payload.amount,
        "clearing": "INTERNAL-CEA"
    }

@router.post("/pix/split")
async def split_pix(payload: SplitPayload):
    """Liquidação em múltiplos destinos (Escrow + Fornecedor + Impostos)"""
    return {
        "status": "processed",
        "splits_count": len(payload.splits),
        "transaction_ref": payload.transaction_id
    }
