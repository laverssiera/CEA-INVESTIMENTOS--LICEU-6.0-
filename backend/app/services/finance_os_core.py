from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from backend.app.models.finance_core import Wallet, LedgerEntry
import uuid

class FinanceOSService:
    def __init__(self, db: Session):
        self.db = db

    def create_wallet(self, owner_id: str, owner_type: str, currency: str = "BRL") -> Wallet:
        wallet = Wallet(
            owner_id=owner_id,
            owner_type=owner_type,
            currency=currency,
            balance=Decimal("0.0")
        )
        self.db.add(wallet)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet

    def process_transaction(self, from_wallet_id: int, to_wallet_id: int, amount: Decimal, description: str):
        """Processa uma transação de partida dobrada entre duas wallets"""
        tx_id = str(uuid.uuid4())
        
        # Débito
        debit_entry = LedgerEntry(
            transaction_id=tx_id,
            wallet_id=from_wallet_id,
            entry_type="debit",
            amount=amount,
            description=f"Saída: {description}",
            account_code="INTERNAL_TRANSFER"
        )
        
        # Crédito
        credit_entry = LedgerEntry(
            transaction_id=tx_id,
            wallet_id=to_wallet_id,
            entry_type="credit",
            amount=amount,
            description=f"Entrada: {description}",
            account_code="INTERNAL_TRANSFER"
        )
        
        # Atualização de saldos reais nas wallets
        from_wallet = self.db.query(Wallet).filter(Wallet.id == from_wallet_id).first()
        to_wallet = self.db.query(Wallet).filter(Wallet.id == to_wallet_id).first()
        
        if from_wallet.balance < amount and from_wallet.owner_type != 'holding':
            raise ValueError("Saldo insuficiente para operação institucional.")
            
        from_wallet.balance -= amount
        to_wallet.balance += amount
        
        self.db.add_all([debit_entry, credit_entry, from_wallet, to_wallet])
        self.db.commit()
        
        return tx_id
