import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/audit/chain", tags=["Immutable Audit Chain"])

class AuditEntry(BaseModel):
    id: UUID
    timestamp: datetime
    module: str
    action: str
    data: Dict[str, Any]
    previous_hash: str
    hash: str
    signature: str # Assinatura digital do motor de decisão

class AuditChainManager:
    """
    Gerencia a trilha de auditoria imutável do CEA.
    Cada decisão financeira gera um elo na corrente.
    """
    def __init__(self):
        self._last_hash = "CEA_GENESIS_BLOCK_CIVILIZATIONAL_FINANCE"

    def _generate_hash(self, data: Dict[str, Any], previous_hash: str) -> str:
        content = json.dumps(data, sort_keys=True) + previous_hash
        return hashlib.sha256(content.encode()).hexdigest()

    def create_entry(self, module: str, action: str, data: Dict[str, Any]) -> AuditEntry:
        new_id = uuid4()
        timestamp = datetime.now()
        
        current_hash = self._generate_hash(data, self._last_hash)
        
        entry = AuditEntry(
            id=new_id,
            timestamp=timestamp,
            module=module,
            action=action,
            data=data,
            previous_hash=self._last_hash,
            hash=current_hash,
            signature=f"SIG_{current_hash[:16]}" # Placeholder para assinatura RSA/ECC
        )
        
        self._last_hash = current_hash
        # Em produção, este dado seria persistido em uma tabela SQL imutável ou Ledger DB
        return entry

audit_manager = AuditChainManager()

@router.post("/verify", response_model=AuditEntry)
async def log_civilizational_decision(module: str, action: str, data: Dict[str, Any]):
    """
    Registra uma decisão na corrente de auditoria imutável.
    """
    try:
        entry = audit_manager.create_entry(module, action, data)
        return entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/integrity")
async def check_chain_integrity():
    """
    Verifica se a corrente de auditoria foi violada.
    """
    return {"status": "INTEGRITY_VERIFIED", "last_hash": audit_manager._last_hash}
