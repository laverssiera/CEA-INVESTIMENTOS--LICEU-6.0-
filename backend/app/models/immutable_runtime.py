import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, String, JSON, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ImmutableEvent(Base):
    """
    Core model for Immutable Financial Runtime (ISSUE-CEA-002)
    Implements a hash chain to ensure event integrity.
    """
    __tablename__ = "immutable_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Chaining
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=True)
    current_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    
    # Metadata
    sequence: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)

    def calculate_hash(self) -> str:
        content = {
            "event_type": self.event_type,
            "payload": self.payload,
            "previous_hash": self.previous_hash,
            "sequence": self.sequence,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        encoded = json.dumps(content, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

class FinancialSnapshot(Base):
    """Snapshot for faster replay reconstruction"""
    __tablename__ = "financial_snapshots"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    last_event_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    state_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
