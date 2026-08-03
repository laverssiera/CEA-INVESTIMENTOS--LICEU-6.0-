from __future__ import annotations

from nats.aio.client import Client as NATS

from apps.cea.core.config import settings

nc = NATS()
_js = None


async def connect_nats() -> NATS:
    if not nc.is_connected:
        await nc.connect(servers=[settings.NATS_URL])
    return nc


async def get_jetstream():
    global _js
    client = await connect_nats()
    if _js is None:
        _js = client.jetstream()
    return _js
