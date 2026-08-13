from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.automation_storage import append_notification, fetch_notifications

NOTIFICATION_LOG: list[dict[str, Any]] = []
CHANNELS = {"email", "whatsapp", "push", "dashboard"}


def send_notification(channel: str, trigger: str, recipient: str, message: str) -> dict[str, Any]:
    if channel not in CHANNELS:
        raise ValueError(f"Canal nao suportado: {channel}")

    item = {
        "id": f"NTF-{len(NOTIFICATION_LOG) + 1:05d}",
        "channel": channel,
        "trigger": trigger,
        "recipient": recipient,
        "message": message,
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "status": "sent",
    }
    NOTIFICATION_LOG.append(item)
    append_notification(item)
    return item


def latest_notifications(limit: int = 100) -> list[dict[str, Any]]:
    stored = fetch_notifications(limit)
    return stored if stored else NOTIFICATION_LOG[-limit:]
