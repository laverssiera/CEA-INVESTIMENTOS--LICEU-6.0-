import json

from sqlalchemy.orm import Session

from app.models import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, action: str, username: str, role: str, payload: dict | None = None) -> AuditLog:
        entry = AuditLog(action=action, username=username, role=role, payload=json.dumps(payload or {}))
        self.db.add(entry)
        self.db.flush()
        return entry
