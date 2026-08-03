from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.modules.notifications.service import latest_notifications, send_notification

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


class NotificationInput(BaseModel):
    channel: str = Field(pattern="^(email|whatsapp|push|dashboard)$")
    trigger: str
    recipient: str
    message: str


@router.post("/send")
def send(payload: NotificationInput) -> dict[str, Any]:
    return send_notification(payload.channel, payload.trigger, payload.recipient, payload.message)


@router.get("/logs")
def logs() -> dict[str, Any]:
    return {"items": latest_notifications()}
