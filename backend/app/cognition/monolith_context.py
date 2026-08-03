from typing import Dict, Any
from datetime import datetime, timezone

class MonolithContext:
    """
    Gestor de contexto local do monólito CEA para sincronização global
    """
    def __init__(self):
        self.local_state = {}

    def get_context_summary(self):
        """
        Retorna resumo do estado local do CEA para o John
        """
        return {
            "monolith": "cea",
            "uptime": True,
            "financial_state": "stable",
            "active_projects": 42,
            "risk_level": "moderate",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def update_global_policy(self, policy: Dict[str, Any]):
        """
        Atualiza política local vinda do John Monólito
        """
        self.local_state["global_policy"] = policy
        return {"policy_updated": True, "at": datetime.now(timezone.utc).isoformat()}
