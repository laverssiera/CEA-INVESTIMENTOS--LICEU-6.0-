from collections import deque
from datetime import datetime, timezone


class EcosystemMemory:
    def __init__(self, max_items=100000):
        self.memory = deque(maxlen=max_items)


    def remember(self, category, payload):
        self.memory.append({
            "category": category,
            "payload": payload,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })


    def recent(self, limit=100):
        return list(self.memory)[-limit:]
