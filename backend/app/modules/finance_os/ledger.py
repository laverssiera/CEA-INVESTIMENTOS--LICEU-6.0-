from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class EntryType(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class LedgerEntry(BaseModel):
    account_id: str
    amount: Decimal
    entry_type: EntryType
    description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = {}

class Transaction(BaseModel):
    transaction_id: str
    entries: List[LedgerEntry]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FinanceOSLedger:
    """
    Motor de Contabilidade de Partidas Dobradas (Double-Entry Ledger).
    Garante que a soma dos débitos seja igual à soma dos créditos.
    """
    
    def validate_transaction(self, transaction: Transaction) -> bool:
        total = Decimal("0.0")
        for entry in transaction.entries:
            if entry.entry_type == EntryType.CREDIT:
                total += entry.amount
            else:
                total -= entry.amount
        return total == Decimal("0.0")

    async def record_transaction(self, transaction: Transaction):
        if not self.validate_transaction(transaction):
            raise ValueError("Invalid transaction: unbalanced debit/credit")
        
        # Aqui integraria com o PostgreSQL via SQLAlchemy
        # e dispararia eventos NATS para sincronização
        print(f"Transaction {transaction.transaction_id} recorded successfully.")
        return True

    def get_account_balance(self, account_id: str) -> Decimal:
        # Mock de saldo
        return Decimal("1000000.00")
