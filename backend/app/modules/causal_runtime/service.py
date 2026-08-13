class CausalRuntime:
    def __init__(self):
        self.causal_links = []


    def register_cause(self, source_event, target_event, confidence=0.5):
        self.causal_links.append({
            "source": source_event,
            "target": target_event,
            "confidence": confidence
        })


    def explain(self, target_event):
        return [
            c for c in self.causal_links
            if c["target"] == target_event
        ]
