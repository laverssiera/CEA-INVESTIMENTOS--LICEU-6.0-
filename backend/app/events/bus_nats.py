import nats
from nats.js.api import StreamConfig, RetentionPolicy
import json
import logging

class CEAEventBus:
    def __init__(self, nats_url="nats://localhost:4222"):
        self.nats_url = nats_url
        self.nc = None
        self.js = None

    async def connect(self):
        self.nc = await nats.connect(self.nats_url)
        self.js = self.nc.jetstream()
        
        # Configura o Stream Principal do CEA
        await self.js.add_stream(
            name="CEA_EVENTS", 
            subjects=["cea.*"],
            config=StreamConfig(
                retention=RetentionPolicy.LIMITS,
                max_msgs=1000000
            )
        )

    async def publish_event(self, subject: str, data: dict):
        if not self.js:
            await self.connect()
        
        payload = json.dumps(data).encode()
        await self.js.publish(f"cea.{subject}", payload)
        logging.info(f"Evento publicado: cea.{subject}")

    async def disconnect(self):
        if self.nc:
            await self.nc.drain()
