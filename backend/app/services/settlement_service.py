from sqlalchemy.orm import Session
from app.models.financial_contracts import FinancialContract, LedgerContract, TreasuryContract, SettlementContract
from app.schemas.financial_contracts import FinancialContractCreate, LedgerContractCreate, TreasuryContractCreate, SettlementContractCreate
from datetime import datetime, timezone

class SettlementService:
    def __init__(self, db: Session):
        self.db = db

    def create_ledger_contract(self, data: LedgerContractCreate) -> LedgerContract:
        contract = LedgerContract(
            **data.model_dump(),
            contract_type="ledger"
        )
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def create_treasury_contract(self, data: TreasuryContractCreate) -> TreasuryContract:
        contract = TreasuryContract(
            **data.model_dump(),
            contract_type="treasury"
        )
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def create_settlement_contract(self, data: SettlementContractCreate) -> SettlementContract:
        contract = SettlementContract(
            **data.model_dump(),
            contract_type="settlement"
        )
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def settle_contract(self, contract_id: str):
        contract = self.db.query(FinancialContract).filter(FinancialContract.id == contract_id).first()
        if contract:
            contract.status = "settled"
            contract.actual_settlement_at = datetime.now(timezone.utc)
            self.db.commit()
            return contract
        return None
