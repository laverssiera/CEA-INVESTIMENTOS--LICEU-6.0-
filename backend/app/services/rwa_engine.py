from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.rwa_core import RWAAsset, RWAToken
from backend.app.services.finance_os_core import FinanceOSService

class RWATokenizationService:
    def __init__(self, db: Session):
        self.db = db
        self.finance_os = FinanceOSService(db)

    def securitize_project(self, project_id: str, name: str, valuation: Decimal, asset_type: str = "real_estate"):
        """Transforma um projeto de engenharia (ARCHIMEDES) em um ativo RWA tokenizado"""
        
        # 1. Cria o Ativo RWA
        asset = RWAAsset(
            name=name,
            asset_type=asset_type,
            valuation=valuation,
            token_total_supply=valuation, # 1 token = 1 BRL (exemplo de stable-asset)
            token_price=Decimal("1.00"),
            origin_project_id=project_id,
            status="active"
        )
        self.db.add(asset)
        self.db.flush() # Para pegar o ID
        
        # 2. Emite os tokens iniciais na Wallet da Holding
        holding_wallet = self.finance_os.create_wallet(
            owner_id="LICEU_HOLDING",
            owner_type="holding",
            currency="BRL"
        ) # Simplificado: buscaria uma existente na realidade
        
        token_entry = RWAToken(
            asset_id=asset.id,
            wallet_id=holding_wallet.id,
            balance=asset.token_total_supply
        )
        
        self.db.add(token_entry)
        self.db.commit()
        return asset

    def distribute_yield(self, asset_id: int, total_profit: Decimal):
        """Distribui lucro do ativo para todos os detentores de tokens"""
        asset = self.db.query(RWAAsset).filter(RWAAsset.id == asset_id).first()
        holders = self.db.query(RWAToken).filter(RWAToken.asset_id == asset_id).all()
        
        for holder in holders:
            # Rendimento PRO-RATA
            participation_pct = holder.balance / asset.token_total_supply
            holder_yield = total_profit * participation_pct
            
            # Crédito na Wallet Financeira do investidor
            self.finance_os.process_transaction(
                from_wallet_id=1, # Central Finance Wallet ID (Exemplo)
                to_wallet_id=holder.wallet_id,
                amount=holder_yield,
                description=f"Distribuição Yield RWA: {asset.name}"
            )
        
        self.db.commit()
