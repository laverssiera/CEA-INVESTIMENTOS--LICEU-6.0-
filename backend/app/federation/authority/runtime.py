import json
import socket

from nats.aio.client import Client as NATS

from backend.app.federation.config import settings

class FederationAuthority:

    def __init__(self):
        self.nc = NATS()

    async def connect(self):
        await self.nc.connect(settings.NATS_URL)

    async def register(self):

        payload = {

            "monolith": "cea-investimentos",

            "host": socket.gethostname(),

            "domains": [

                "finance-os",
                "treasury",
                "underwriting",
                "risk-engine",
                "banking-compliance",
                "aml",
                "kyc",
                "rwa-engine",
                "digital-wallet",
                "institutional-banking",
                "orbital-banking",
                "interplanetary-treasury"

            ]
        }

        await self.nc.publish(
            "federation.runtime.register",
            json.dumps(payload).encode()
        )
