import nats
from nats.js.api import StreamConfig, RetentionPolicy
import json

class EventBus:
    """Barramento de Eventos Institucional NATS/JetStream"""
    def __init__(self, nats_url="nats://localhost:4222"):
        self.nats_url = nats_url
        self.nc = None
        self.js = None

    async def connect(self):
        self.nc = await nats.connect(self.nats_url)
        self.js = self.nc.jetstream()

    async def publish(self, subject: str, payload: dict):
        if not self.js:
            await self.connect()
        
        # Converte payload e garante padrão CEA
        await self.js.publish(
            f"cea.{subject}", 
            json.dumps(payload).encode()
        )

    async def disconnect(self):
        if self.nc:
            await self.nc.close()
