from decimal import Decimal
import random

class EcosystemCreditScoreService:
    @staticmethod
    async def calculate_score(entity_id: str, opera_data: dict, archimedes_data: dict) -> dict:
        """
        Calcula o score de crédito baseado em dados OPERACIONAIS REAIS.
        Diferencial CEA: Não depende apenas de Serasa/Balanço.
        """
        
        # Fatores Operacionais
        delivery_on_time = opera_data.get('delivery_rate', 0.95) # % de entregas no prazo
        error_rate = opera_data.get('error_rate', 0.02) # % de falhas técnicas
        reputation_score = opera_data.get('reputation', 9.0) # Avaliação ARCHIMEDES
        
        # Cálculo Base (Exemplo de Heurística)
        base_score = 600
        
        # Bônus por eficiência logistica e produtiva
        performance_bonus = (delivery_on_time * 200) - (error_rate * 500)
        reputation_bonus = reputation_score * 20
        
        final_score = base_score + performance_bonus + reputation_bonus
        
        # Garantindo limites (0 - 1000)
        final_score = max(0, min(1000, final_score))
        
        return {
            "entity_id": entity_id,
            "ecosystem_score": round(final_score, 2),
            "tier": "PREMIUM" if final_score > 850 else "INSTITUTIONAL" if final_score > 700 else "RELIABLE",
            "factors": {
                "opera_delivery": delivery_on_time,
                "technical_precision": 1 - error_rate,
                "archimedes_trust": reputation_score
            }
        }
