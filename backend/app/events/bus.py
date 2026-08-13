from __future__ import annotations

import uuid
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Callable

from app.events.nats_runtime import FinanceNatsRuntime
from app.runtime.investments import InvestmentNetworkRuntime
from app.services.automation_storage import append_event, record_event_dispatch, was_event_dispatched

EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)
        self._history: list[dict[str, Any]] = []
        self._nats = FinanceNatsRuntime()
        self._investment_network = InvestmentNetworkRuntime()

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._subscribers[event_name].append(handler)

    def publish(
        self,
        event_name: str,
        payload: dict[str, Any] | None = None,
        *,
        propagate_nats: bool = True,
        event_id: str | None = None,
    ) -> None:
        current_event_id = event_id or f"EVT-{uuid.uuid4()}"
        event = {
            "id": current_event_id,
            "event": event_name,
            "payload": payload or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._history.append(event)
        append_event(event_name, event["payload"], event_id=current_event_id)

        if event_name.startswith("investment."):
            self._investment_network.ingest_investment_event(event)

        if propagate_nats:
            self._nats.publish(event_name=event_name, payload=event["payload"], event_id=current_event_id)

        for handler in self._subscribers.get(event_name, []):
            handler(event)

    def history(self, limit: int = 200) -> list[dict[str, Any]]:
        return self._history[-limit:]

    def investment_network_summary(self) -> dict[str, Any]:
        return self._investment_network.summarize_network()


event_bus = EventBus()


async def _handle_nats_event(event_name: str, payload: dict[str, Any], event_id: str | None) -> None:
    external_event_id = event_id or f"NATS-{uuid.uuid4()}"
    if was_event_dispatched(external_event_id, transport="nats-consumer"):
        return

    data = dict(payload or {})
    data.setdefault("source_bus", "nats")

    event_bus.publish(
        event_name=event_name,
        payload=data,
        propagate_nats=False,
        event_id=external_event_id,
    )
    record_event_dispatch(event_id=external_event_id, transport="nats-consumer", status="success")


async def start_nats_consumer() -> bool:
    return await event_bus._nats.start_consumer(_handle_nats_event)


async def stop_nats_consumer() -> None:
    await event_bus._nats.stop()
