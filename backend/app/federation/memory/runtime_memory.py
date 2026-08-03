import redis
import json

from backend.app.federation.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

class FinancialMemory:

    @staticmethod
    def save_event(event_id, payload):

        redis_client.set(
            f"cea:event:{event_id}",
            json.dumps(payload)
        )
