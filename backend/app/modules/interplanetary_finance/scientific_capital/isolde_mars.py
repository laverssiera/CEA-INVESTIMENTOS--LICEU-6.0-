import numpy as np
from typing import Dict, Any, List

class IsoldeMarsFinance:
    def __init__(self):
        # Valores base em Bilhões de Dólares (USD)
        self.capex_breakdown = {
            "infraestrutura_base": 30.0,
            "laboratorios_nucleares": 15.0,
            "logistica_lancamento": 20.0,
            "blindagem_radiologica_inicial": 10.0
        }
        self.total_capex = sum(self.capex_breakdown.values())
        
        self.annual_opex = {
            "manutencao_sistemas": 2.0,
            "logistica_suprimentos": 3.0,
            "operacoes_pesquisa": 1.5,
            "seguranca_radiologica": 0.5
        }
        self.total_annual_opex = sum(self.annual_opex.values())
        
        self.revenue_streams = {
            "pesquisa_nucleos_exoticos": 10.0, # Breakthroughs energéticos e médicos
            "descoberta_materiais": 6.0,      # Novos semicondutores e supercondutores
            "licenciamento_blindagem": 5.0,   # Venda de tech para outras agências
            "construcao_civil_cea": 7.0       # Produção local de materiais de construção
        }
        self.total_annual_revenue = sum(self.revenue_streams.values())

    def calculate_metrics(self, years: int = 15, discount_rate: float = 0.12) -> Dict[str, Any]:
        # Fluxo de Caixa: Investimento inicial negativo no ano 0
        cash_flows = [-self.total_capex]
        
        for year in range(1, years + 1):
            # Ramp-up: Receita começa a subir após o terceiro ano
            revenue_factor = min(1.0, max(0.0, (year - 3) / 2))
            current_revenue = self.total_annual_revenue * revenue_factor
            
            # OPEX é constante a partir do ano 1
            net_flow = current_revenue - self.total_annual_opex
            cash_flows.append(net_flow)
            
        # NPV
        npv = sum(cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows))
        
        # IRR (TIR)
        irr = self._calculate_irr(cash_flows)
        
        # Payback
        cumulative_cf = np.cumsum(cash_flows)
        payback = None
        for i, total in enumerate(cumulative_cf):
            if total >= 0:
                payback = i
                break
                
        return {
            "project_name": "ISOLDE-MARS",
            "capex": round(self.total_capex, 2),
            "opex_anual": round(self.total_annual_opex, 2),
            "receita_anual_plena": round(self.total_annual_revenue, 2),
            "npv": round(float(npv), 2),
            "irr": round(float(irr), 4),
            "payback_years": payback if payback is not None else "N/A",
            "cash_flow_projection": [round(float(cf), 2) for cf in cash_flows],
            "details": {
                "research_focus": "Núcleos Exóticos e Descoberta de Materiais",
                "shielding_tech": "Blindagem de Radiação de Próxima Geração",
                "civil_materials": "Materiais Martianos para Engenharia Civil (CEA)"
            }
        }

    def _calculate_irr(self, cash_flows: List[float], iterations: int = 1000) -> float:
        rate = 0.1
        for _ in range(iterations):
            npv = sum(cf / (1 + rate)**i for i, cf in enumerate(cash_flows))
            if abs(npv) < 0.01:
                return rate
            derivative = sum(-i * cf / (1 + rate)**(i + 1) for i, cf in enumerate(cash_flows))
            if derivative == 0:
                break
            rate = rate - npv / derivative
        return rate
