from __future__ import annotations

import os
from datetime import datetime, timezone

import jwt
from fastapi import APIRouter, HTTPException
from fastapi import Depends, Header, status as http_status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import get_db
from app.events import event_bus
from app.models.entities import InterplanetaryDomain


router = APIRouter(prefix="/interplanetary")

INTERPLANETARY_ECOSYSTEM_DOMAINS: list[dict[str, str]] = [
    {
        "id": "cea",
        "name": "CEA",
        "type": "governance-hub",
        "subject": "cea.interplanetary.cea",
        "description": "Nucleo de coordenacao financeira e governanca do ecossistema.",
    },
    {
        "id": "interplanetary-bank",
        "name": "Interplanetary Bank",
        "type": "banking",
        "subject": "cea.interplanetary.bank",
        "description": "Operacoes bancarias multi-jurisdicao para habitats terrestres e espaciais.",
    },
    {
        "id": "interplanetary-investment",
        "name": "Interplanetary Investment",
        "type": "asset-management",
        "subject": "cea.interplanetary.investment",
        "description": "Alocacao de capital para infraestrutura, ciencia e tecnologia de fronteira.",
    },
    {
        "id": "space-exchange",
        "name": "Space Exchange",
        "type": "marketplace",
        "subject": "cea.interplanetary.space_exchange",
        "description": "Ambiente de negociacao para ativos espaciais, contratos e liquidez orbital.",
    },
    {
        "id": "patent-exchange",
        "name": "Patent Exchange",
        "type": "intellectual-property",
        "subject": "cea.interplanetary.patent_exchange",
        "description": "Mercado de licenciamento e monetizacao de patentes estrategicas.",
    },
    {
        "id": "technology-exchange",
        "name": "Technology Exchange",
        "type": "innovation-transfer",
        "subject": "cea.interplanetary.technology_exchange",
        "description": "Canal de transferencia e precificacao de tecnologias entre instituicoes.",
    },
    {
        "id": "space-insurance",
        "name": "Space Insurance",
        "type": "risk-transfer",
        "subject": "cea.interplanetary.space_insurance",
        "description": "Cobertura de riscos operacionais, climaticos e orbitais em missoes.",
    },
]

INTERPLANETARY_ACTIVATION_RBAC: dict[str, set[str]] = {
    "cea": {"admin", "governance", "diretoria"},
    "interplanetary-bank": {"admin", "tesouraria", "risk_manager", "governance", "diretoria"},
    "interplanetary-investment": {"admin", "risk_manager", "governance", "diretoria"},
    "space-exchange": {"admin", "risk_manager", "governance", "diretoria"},
    "patent-exchange": {"admin", "governance", "diretoria"},
    "technology-exchange": {"admin", "governance", "diretoria"},
    "space-insurance": {"admin", "risk_manager", "governance", "diretoria"},
}

SECRET_KEY = os.getenv("CEA_SECRET_KEY", "cea-liceu-6-financial-engine")
ALGORITHM = "HS256"


def _get_domain_or_404(domain_id: str) -> dict[str, str]:
    domain = next((item for item in INTERPLANETARY_ECOSYSTEM_DOMAINS if item["id"] == domain_id), None)
    if domain is None:
        raise HTTPException(status_code=404, detail="Interplanetary domain not found")
    return domain


def _ensure_domains_seeded(db: Session) -> None:
    Base.metadata.create_all(bind=db.get_bind(), tables=[InterplanetaryDomain.__table__])

    existing = set(db.execute(select(InterplanetaryDomain.domain_id)).scalars().all())
    if len(existing) == len(INTERPLANETARY_ECOSYSTEM_DOMAINS):
        return

    for item in INTERPLANETARY_ECOSYSTEM_DOMAINS:
        if item["id"] in existing:
            continue
        db.add(
            InterplanetaryDomain(
                domain_id=item["id"],
                name=item["name"],
                domain_type=item["type"],
                subject=item["subject"],
                description=item["description"],
                status="active" if item["id"] == "cea" else "planned",
                active=item["id"] == "cea",
            )
        )
    db.commit()


def _decode_token(token: str) -> dict[str, str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Token invalido") from exc

    if payload.get("type") and payload.get("type") != "access":
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Tipo de token invalido")
    return payload


def _resolve_actor_role(
    authorization: str | None,
    x_interplanetary_role: str | None,
) -> tuple[str, str]:
    if x_interplanetary_role:
        return "internal-header", x_interplanetary_role.lower()

    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Bearer token obrigatorio")

    token = authorization.split(" ", 1)[1]
    payload = _decode_token(token)
    role = str(payload.get("role") or "").lower().strip()
    user = str(payload.get("sub") or "unknown")
    if not role:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Role ausente no token")
    return user, role


def _require_activation_role(domain_id: str, role: str) -> None:
    allowed = INTERPLANETARY_ACTIVATION_RBAC.get(domain_id, {"admin"})
    if role not in allowed:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail="Sem permissao para ativar este dominio")


@router.get("/status")
async def status():
    return {
        "runtime": "online",
        "federation": "connected",
        "knowledge_graph": "active",
        "ecosystem_memory": "active",
        "causal_runtime": "active"
    }


@router.get("/ecosystem")
async def ecosystem_domains(db: Session = Depends(get_db)) -> dict[str, object]:
    _ensure_domains_seeded(db)
    rows = db.execute(select(InterplanetaryDomain).order_by(InterplanetaryDomain.name.asc())).scalars().all()
    return {
        "count": len(rows),
        "items": [
            {
                "id": row.domain_id,
                "name": row.name,
                "type": row.domain_type,
                "subject": row.subject,
                "description": row.description,
                "status": row.status,
                "active": row.active,
                "last_activation_at": row.last_activation_at.isoformat() if row.last_activation_at else None,
            }
            for row in rows
        ],
    }


@router.get("/ecosystem/{domain_id}")
async def ecosystem_domain(domain_id: str, db: Session = Depends(get_db)) -> dict[str, str | bool | None]:
    _ensure_domains_seeded(db)
    row = db.execute(select(InterplanetaryDomain).where(InterplanetaryDomain.domain_id == domain_id)).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Interplanetary domain not found")
    return {
        "id": row.domain_id,
        "name": row.name,
        "type": row.domain_type,
        "subject": row.subject,
        "description": row.description,
        "status": row.status,
        "active": row.active,
        "last_activation_at": row.last_activation_at.isoformat() if row.last_activation_at else None,
    }


@router.post("/ecosystem/{domain_id}/activate")
async def activate_ecosystem_domain(
    domain_id: str,
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
    x_interplanetary_role: str | None = Header(default=None),
) -> dict[str, str]:
    _ensure_domains_seeded(db)
    domain = db.execute(select(InterplanetaryDomain).where(InterplanetaryDomain.domain_id == domain_id)).scalar_one_or_none()
    if domain is None:
        raise HTTPException(status_code=404, detail="Interplanetary domain not found")

    actor_user, actor_role = _resolve_actor_role(authorization=authorization, x_interplanetary_role=x_interplanetary_role)
    _require_activation_role(domain_id=domain_id, role=actor_role)

    domain.status = "active"
    domain.active = True
    domain.last_activation_at = datetime.now(timezone.utc)
    db.add(domain)
    db.commit()

    event_bus.publish(
        "cea.interplanetary.domain.activated",
        {
            "domain_id": domain.domain_id,
            "domain_name": domain.name,
            "subject": domain.subject,
            "actor_user": actor_user,
            "actor_role": actor_role,
        },
    )
    return {
        "status": "activated",
        "domain_id": domain.domain_id,
        "event": "cea.interplanetary.domain.activated",
    }
