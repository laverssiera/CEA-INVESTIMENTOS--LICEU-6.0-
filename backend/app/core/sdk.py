from typing import List, Dict, Any
from app.modules.federation_authority.service import FederationAuthorityService
from app.modules.knowledge_graph.service import FinancialKnowledgeGraph
from app.modules.unified_observability.service import UnifiedObservability
from app.modules.sovereign_compliance.service import SovereignComplianceEngine
from app.modules.rwa_cosmic_engine.service import RWACosmicEngine

class CEAUnifiedSDK:
    """
    SDK Unificado para integração do CEA Investimentos com outros monólitos (JURIDICOTECH, ECONOTECH, etc).
    """
    def __init__(self, nats_client=None):
        self.federation = FederationAuthorityService(nats_client)
        self.graph = FinancialKnowledgeGraph()
        self.observability = UnifiedObservability()
        self.compliance = SovereignComplianceEngine()
        self.rwa = RWACosmicEngine()

    async def execute_interplanetary_operation(self, operation_data: Dict[str, Any]):
        # 1. Trace inicial
        self.observability.trace("CEA_SDK", "operation_start", "processing", operation_data)
        
        # 2. Validação de Compliance Soberano
        compliance_payload = {
            "amount": operation_data.get("valuation", 0),
            "offshore": operation_data.get("planetary_origin") != "Terra",
            "tokenized_asset": operation_data.get("tokenize", False)
        }
        compliance_check = self.compliance.validate_operation(compliance_payload)
        if not compliance_check["approved"]:
            self.observability.trace("CEA_SDK", "operation_failed", "compliance_rejected", compliance_check)
            return {"status": "rejected", "reason": "Compliance failure", "compliance": compliance_check}

        # 3. Tokenização RWA se necessário
        token_data = None
        if operation_data.get("tokenize"):
            token_data = self.rwa.tokenize_asset(
                operation_data["asset_name"], 
                operation_data["valuation"], 
                operation_data.get("planetary_origin", "Terra")
            )
            self.graph.add_entity(token_data["token_id"], "RWA_TOKEN", token_data)

        # 4. Registro no Knowledge Graph
        self.graph.add_entity(operation_data["operation_id"], "FINANCIAL_OP", operation_data)
        
        self.observability.trace("CEA_SDK", "operation_success", "completed", {"token": token_data})
        
        return {
            "status": "success",
            "compliance": compliance_check,
            "token": token_data,
            "topology": self.graph.build_credit_topology()
        }
