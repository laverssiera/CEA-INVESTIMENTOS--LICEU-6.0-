from __future__ import annotations

import json

from nats.js.api import ConsumerConfig, DeliverPolicy

from apps.cea.core.config import settings
from apps.cea.core.database import SessionLocal
from apps.cea.core.nats import get_jetstream
from apps.cea.modules.investment.service import evaluate_event

SUBJECTS = [
    "archimedes.deal_created",
    "gamemkt.campaign_started",
    "hub.cost_registered",
]


async def start_consumers() -> None:
    js = await get_jetstream()

    try:
        await js.add_stream(name=settings.NATS_STREAM, subjects=SUBJECTS)
    except Exception:
        # Stream ja pode existir em ambientes compartilhados.
        pass

    async def handler(msg):
        db = SessionLocal()
        try:
            data = json.loads(msg.data.decode())
            await evaluate_event(db, msg.subject, data)
            await msg.ack()
        except Exception:
            await msg.nak()
        finally:
            db.close()

    for subject in SUBJECTS:
        await js.subscribe(
            subject,
            cb=handler,
            durable=f"{settings.NATS_CONSUMER}_{subject.replace('.', '_')}",
            config=ConsumerConfig(deliver_policy=DeliverPolicy.ALL),
            stream=settings.NATS_STREAM,
            manual_ack=True,
        )
