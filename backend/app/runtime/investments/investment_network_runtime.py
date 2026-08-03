from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import networkx as nx


class InvestmentNetworkRuntime:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def register_entity(self, entity_id: str, entity_type: str, **attributes: Any) -> dict[str, Any]:
        node_payload = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            **attributes,
        }
        self.graph.add_node(entity_id, **node_payload)
        return node_payload

    def register_relationship(
        self,
        source_entity: str,
        target_entity: str,
        relationship_type: str,
        *,
        weight: float = 1.0,
        **attributes: Any,
    ) -> dict[str, Any]:
        edge_payload = {
            "relationship_type": relationship_type,
            "weight": weight,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **attributes,
        }
        self.graph.add_edge(source_entity, target_entity, **edge_payload)
        return edge_payload

    def ingest_investment_event(self, event: dict[str, Any]) -> dict[str, Any]:
        payload = dict(event.get("payload", {}))
        investor_id = payload.get("investor_id") or payload.get("user_id") or "unknown_investor"
        asset_id = payload.get("asset_id") or payload.get("project_id") or "unknown_asset"
        amount = float(payload.get("amount", 0.0))

        self.register_entity(investor_id, "investor", amount=amount)
        self.register_entity(asset_id, "asset", amount=amount)
        self.register_relationship(
            investor_id,
            asset_id,
            event.get("event", "investment.event"),
            weight=amount,
            event_id=event.get("id"),
        )

        return {
            "status": "ingested",
            "event_id": event.get("id"),
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
        }

    def summarize_network(self) -> dict[str, Any]:
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": round(nx.density(self.graph), 4) if self.graph.number_of_nodes() > 1 else 0.0,
            "components": nx.number_weakly_connected_components(self.graph) if self.graph.number_of_nodes() else 0,
            "captured_at": datetime.now(timezone.utc).isoformat(),
        }


if __name__ == "__main__":
    runtime = InvestmentNetworkRuntime()
    runtime.ingest_investment_event(
        {
            "id": "EVT-DEMO-001",
            "event": "investment.created",
            "payload": {
                "investor_id": "CEA-CENTRAL",
                "asset_id": "RWA-001",
                "amount": 250000,
            },
        }
    )
    print(runtime.summarize_network())