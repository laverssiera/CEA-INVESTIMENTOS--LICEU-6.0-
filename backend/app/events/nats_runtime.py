from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any

from app.services.automation_storage import record_event_dispatch, was_event_dispatched

NatsHandler = Callable[[str, dict[str, Any], str | None], Awaitable[None]]


class FinanceNatsRuntime:
    def __init__(self) -> None:
        self.enabled = os.getenv("FINANCE_NATS_ENABLED", "false").lower() == "true"
        self.consumer_enabled = os.getenv("FINANCE_NATS_CONSUMER_ENABLED", "false").lower() == "true"
        self.nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
        self.subject_prefix = os.getenv("FINANCE_NATS_PREFIX", "cea")
        self.stream_name = os.getenv("FINANCE_NATS_STREAM", "CEA_FINANCE_EVENTS")
        self.queue_group = os.getenv("FINANCE_NATS_QUEUE_GROUP", "cea-finance-consumers")
        self.retry_max_attempts = max(1, int(os.getenv("FINANCE_NATS_RETRY_MAX_ATTEMPTS", "3")))
        self.retry_backoff_seconds = max(0.1, float(os.getenv("FINANCE_NATS_RETRY_BACKOFF_SECONDS", "0.5")))

        raw_subjects = os.getenv(
            "FINANCE_NATS_CONSUME_SUBJECTS",
            "archimedes.deal_created,gamemkt.campaign_started,hub.cost_registered",
        )
        self.consume_subjects = [item.strip() for item in raw_subjects.split(",") if item.strip()]

        self._nats = None
        self._subscriptions: list[Any] = []

    async def _connect(self) -> bool:
        if self._nats is not None and getattr(self._nats, "is_connected", False):
            return True

        try:
            import nats  # type: ignore
        except Exception:
            return False

        try:
            self._nats = await nats.connect(
                self.nats_url,
                connect_timeout=2,
                max_reconnect_attempts=3,
                reconnect_time_wait=1,
            )
            return True
        except Exception:
            self._nats = None
            return False

    async def _ensure_stream(self) -> bool:
        if self._nats is None:
            return False

        try:
            from nats.js.api import StreamConfig
        except Exception:
            return False

        js = self._nats.jetstream()
        try:
            await js.add_stream(
                name=self.stream_name,
                config=StreamConfig(
                    name=self.stream_name,
                    subjects=[f"{self.subject_prefix}.>"],
                    max_msgs=1_000_000,
                ),
            )
        except Exception:
            # Stream pode já existir.
            pass

        return True

    async def _publish_once(self, event_name: str, payload: dict[str, Any], event_id: str) -> bool:
        connected = await self._connect()
        if not connected:
            record_event_dispatch(event_id=event_id, transport="nats", status="failed", error="connect_failed")
            return False

        stream_ready = await self._ensure_stream()
        if not stream_ready:
            record_event_dispatch(event_id=event_id, transport="nats", status="failed", error="stream_unavailable")
            return False

        subject = f"{self.subject_prefix}.{event_name}"
        data = json.dumps(payload).encode("utf-8")

        try:
            js = self._nats.jetstream()
            await js.publish(subject, data, headers={"Nats-Msg-Id": event_id})
            record_event_dispatch(event_id=event_id, transport="nats", status="success")
            return True
        except Exception as exc:
            record_event_dispatch(event_id=event_id, transport="nats", status="failed", error=str(exc))
            return False

    async def _publish_with_retry(self, event_name: str, payload: dict[str, Any], event_id: str) -> None:
        if was_event_dispatched(event_id=event_id, transport="nats"):
            return

        for attempt in range(1, self.retry_max_attempts + 1):
            if was_event_dispatched(event_id=event_id, transport="nats"):
                return

            success = await self._publish_once(event_name=event_name, payload=payload, event_id=event_id)
            if success:
                return

            if attempt < self.retry_max_attempts:
                wait_seconds = self.retry_backoff_seconds * (2 ** (attempt - 1))
                await asyncio.sleep(wait_seconds)

    async def reprocess(self, event_name: str, payload: dict[str, Any], event_id: str) -> dict[str, Any]:
        if not self.enabled:
            return {"status": "skipped", "reason": "nats_disabled"}

        await self._publish_with_retry(event_name=event_name, payload=payload, event_id=event_id)
        if was_event_dispatched(event_id=event_id, transport="nats"):
            return {"status": "reprocessed", "event_id": event_id}

        return {"status": "failed", "event_id": event_id}

    def publish(self, event_name: str, payload: dict[str, Any], event_id: str) -> None:
        if not self.enabled:
            return

        if was_event_dispatched(event_id=event_id, transport="nats"):
            return

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._publish_with_retry(event_name, payload, event_id))
        except RuntimeError:
            asyncio.run(self._publish_with_retry(event_name, payload, event_id))

    async def start_consumer(self, handler: NatsHandler) -> bool:
        if not self.enabled or not self.consumer_enabled:
            return False

        connected = await self._connect()
        if not connected:
            return False

        stream_ready = await self._ensure_stream()
        if not stream_ready:
            return False

        async def _callback(msg: Any) -> None:
            subject = getattr(msg, "subject", "")
            event_name = subject.removeprefix(f"{self.subject_prefix}.")
            msg_id = None
            headers = getattr(msg, "headers", None)
            if headers:
                msg_id = headers.get("Nats-Msg-Id")

            try:
                payload = json.loads(msg.data.decode("utf-8")) if msg.data else {}
            except Exception:
                payload = {}

            await handler(event_name, payload, msg_id)

        for item in self.consume_subjects:
            full_subject = f"{self.subject_prefix}.{item}"
            sub = await self._nats.subscribe(full_subject, queue=self.queue_group, cb=_callback)
            self._subscriptions.append(sub)

        return True

    async def stop(self) -> None:
        for sub in self._subscriptions:
            try:
                await sub.unsubscribe()
            except Exception:
                pass
        self._subscriptions = []

        if self._nats is not None:
            try:
                await self._nats.drain()
            except Exception:
                try:
                    await self._nats.close()
                except Exception:
                    pass
            self._nats = None
