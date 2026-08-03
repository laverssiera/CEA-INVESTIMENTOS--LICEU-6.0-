import time


class UnifiedObservability:
    def __init__(self):
        self.events = []


    def trace(self, monolith, action, status, metadata=None):
        self.events.append({
            "timestamp": time.time(),
            "monolith": monolith,
            "action": action,
            "status": status,
            "metadata": metadata or {}
        })


    def metrics(self):
        return {
            "events": len(self.events)
        }
