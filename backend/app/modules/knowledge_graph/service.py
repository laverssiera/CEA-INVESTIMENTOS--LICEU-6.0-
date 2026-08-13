class FinancialKnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []


    def add_entity(self, entity_id, entity_type, metadata=None):
        self.nodes[entity_id] = {
            "type": entity_type,
            "metadata": metadata or {}
        }


    def connect(self, source, target, relation):
        self.edges.append({
            "source": source,
            "target": target,
            "relation": relation
        })


    def build_credit_topology(self):
        return {
            "entities": len(self.nodes),
            "relationships": len(self.edges)
        }
