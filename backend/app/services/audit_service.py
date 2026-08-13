from sqlalchemy.orm import Session

from app.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuditRepository(db)

    def add(self, action: str, username: str, role: str, payload: dict | None = None):
        entry = self.repo.add(action=action, username=username, role=role, payload=payload)
        self.db.commit()
        return entry
