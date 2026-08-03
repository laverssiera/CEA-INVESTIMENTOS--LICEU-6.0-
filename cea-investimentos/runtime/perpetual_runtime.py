import os
import sys
import time
import pandas as pd
import numpy as np
import networkx as nx

# Importando módulos de Governança
from finance.governance.sovereign_financial_governance import SovereignFinancialGovernance
from finance.governance.treasury_consensus_runtime import TreasuryConsensusRuntime
from finance.governance.autonomous_liquidity_regulator import AutonomousLiquidityRegulator

# Importando módulos de Observabilidade
from finance.observability.financial_metrics_runtime import FinancialMetricsRuntime
from finance.observability.financial_integrity_monitor import FinancialIntegrityMonitor

# Importando módulos de Trust
from finance.trust.sovereign_credit_engine import SovereignCreditEngine
from finance.trust.deterministic_financial_validation import DeterministicFinancialValidation

def perpetual_sovereign_intelligence_runtime():
    print("♾️  [PERPETUAL RUNTIME] Evoluindo CEA Investimentos para Inteligência Financeira Perpétua...")
    
    # 1. Governance Layer
    gov = SovereignFinancialGovernance()
    consensus = TreasuryConsensusRuntime()
    regulator = AutonomousLiquidityRegulator()
    
    gov.sync_treasury()
    consensus.coordinate_global_liquidity()
    regulator.balance_pools(1060000, 1060000)
    
    # 2. Observability Layer
    metrics = FinancialMetricsRuntime()
    monitor = FinancialIntegrityMonitor()
    
    current_metrics = metrics.get_realtime_metrics()
    print(f"📊 Métricas em Tempo Real: {current_metrics}")
    monitor.check_integrity()
    
    # 3. Trust Layer
    credit = SovereignCreditEngine()
    validation = DeterministicFinancialValidation()
    
    credit.calculate_credit_limit("GLOBAL-INFRA")
    val_status = validation.validate_proofofsolvency()
    print(f"🛡️ Trust Status: {val_status}")

    print("✅ [PERPETUAL RUNTIME] CEA Investimentos agora opera em modo Perpétuo e Soberano.")

if __name__ == "__main__":
    # Adicionar o diretório atual ao path para facilitar imports relativos no script
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    perpetual_sovereign_intelligence_runtime()
