from datetime import datetime, timezone
from uuid import uuid4


class FederationAuthorityService:
    def __init__(self, nats_client):
        self.nats = nats_client


    async def register_runtime(self, monolith: str, capabilities: list):
        payload = {
            "runtime_id": str(uuid4()),
            "monolith": monolith,
            "capabilities": capabilities,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "classification": "federated-enterprise-runtime"
        }


        await self.nats.publish(
            "federation.runtime.registered",
            str(payload).encode()
        )


        return payload
