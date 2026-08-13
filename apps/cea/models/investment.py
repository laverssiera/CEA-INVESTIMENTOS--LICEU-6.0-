from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from apps.cea.core.database import Base


class InvestmentModel(Base):
    __tablename__ = "investments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)
    expected_roi: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
