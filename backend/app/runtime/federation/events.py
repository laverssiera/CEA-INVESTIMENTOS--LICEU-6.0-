from nats.aio.client import Client as NATS
import asyncio
import json

class FederationBus:

    def __init__(self):
        self.nc = NATS()

    async def connect(self):
        await self.nc.connect("nats://localhost:4222")

    async def publish(self, subject: str, payload: dict):
        await self.nc.publish(
            subject,
            json.dumps(payload).encode()
        )

bus = FederationBus()
