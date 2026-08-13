from __future__ import annotations

import asyncio
import os
from datetime import datetime, timezone
from typing import Any

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException, WebSocket, status
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal
from app.models import InvestmentAsset
from app.repositories.investment_repository import InvestmentRepository
from app.repositories.user_repository import UserRepository
from app.services.investment_service import InvestmentService

router = APIRouter(prefix="/investments", tags=["Home Broker"])
investor_router = APIRouter(prefix="/investor", tags=["Home Broker"])

SECRET_KEY = os.getenv("CEA_SECRET_KEY", "cea-liceu-6-financial-engine")
ALGORITHM = "HS256"

INVESTMENT_ASSETS: list[dict[str, Any]] = [
    {
        "id": 1,
        "symbol": "CEA-LIC-01",
        "name": "Projeto LICEU Industrial",
        "price": 1000,
        "yield": 0.18,
        "risk": "medio",
    },
    {
        "id": 2,
        "symbol": "CEA-LIC-02",
        "name": "Renda RWA Logistica",
        "price": 850,
        "yield": 0.16,
        "risk": "baixo",
    },
]

ORDERS: list[dict[str, Any]] = []


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido") from exc

    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tipo de token invalido")

    return payload


def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token obrigatorio")

    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    return {
        "username": payload.get("sub"),
        "role": payload.get("role", "guest"),
    }


def _ensure_user(db, username: str, role: str) -> int:
    users = UserRepository(db)
    existing = users.get_by_username(username)
    if existing:
        return existing.id

    created = users.create(
        username=username,
        name=username,
        email=f"{username}@cea.local",
        password_hash="external-auth",
        role=role,
    )
    db.commit()
    return created.id


def _assets_from_db_or_memory() -> list[dict[str, Any]]:
    try:
        with SessionLocal() as db:
            repo = InvestmentRepository(db)
            assets = repo.list_assets()
            if assets:
                return [
                    {
                        "id": item.id,
                        "symbol": item.symbol,
                        "name": item.name,
                        "price": float(item.price),
                        "yield": float(item.yield_value),
                        "risk": item.risk,
                    }
                    for item in assets
                ]

            # Seed inicial no banco quando vazio
            for seed in INVESTMENT_ASSETS:
                db.add(
                    InvestmentAsset(
                        symbol=seed["symbol"],
                        name=seed["name"],
                        price=seed["price"],
                        yield_value=seed["yield"],
                        risk=seed["risk"],
                        status="open",
                    )
                )
            db.commit()

            assets = repo.list_assets()
            return [
                {
                    "id": item.id,
                    "symbol": item.symbol,
                    "name": item.name,
                    "price": float(item.price),
                    "yield": float(item.yield_value),
                    "risk": item.risk,
                }
                for item in assets
            ]
    except Exception:
        return INVESTMENT_ASSETS


@router.get("/assets")
def list_assets() -> list[dict[str, Any]]:
    return _assets_from_db_or_memory()


@router.post("/order")
def place_order(order: dict[str, Any], user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    if user["role"] not in {"investor_pf", "investor_pj"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Somente investidor pode enviar ordem")

    try:
        with SessionLocal() as db:
            user_id = _ensure_user(db, user["username"], user["role"])
            service = InvestmentService(db)
            created = service.place_order(
                user_id=user_id,
                asset_id=int(order.get("asset_id", 0)),
                amount=float(order.get("amount", 0)),
            )
            return {
                "status": "ok",
                "order": {
                    "id": created.id,
                    "product_id": created.asset_id,
                    "amount": float(created.amount),
                    "status": created.status,
                },
            }
    except (ValueError, SQLAlchemyError):
        # Fallback in-memory para manter ambiente funcional sem banco
        item = {
            "id": f"HB-{len(ORDERS) + 1:05d}",
            "product_id": order.get("asset_id"),
            "amount": float(order.get("amount", 0)),
            "status": "confirmed",
            "investor": user["username"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        ORDERS.append(item)
        return {"status": "ok", "order": item}


@router.get("/portfolio")
def portfolio(user: dict[str, Any] = Depends(get_current_user)) -> list[dict[str, Any]]:
    try:
        with SessionLocal() as db:
            users = UserRepository(db)
            user_row = users.get_by_username(user["username"])
            if not user_row:
                return []

            repo = InvestmentRepository(db)
            orders = repo.list_orders_by_user(user_row.id)
            assets = {a.id: a for a in repo.list_assets()}
            return [
                {
                    "id": item.id,
                    "product_id": item.asset_id,
                    "product_name": assets[item.asset_id].name if item.asset_id in assets else str(item.asset_id),
                    "amount": float(item.amount),
                    "status": item.status,
                }
                for item in orders
            ]
    except Exception:
        return [i for i in ORDERS if i.get("investor") == user["username"]]


@investor_router.get("/portfolio")
def investor_portfolio(user: dict[str, Any] = Depends(get_current_user)) -> list[dict[str, Any]]:
    return portfolio(user)


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    while True:
        await ws.send_json({"update": "market", "ts": datetime.now(timezone.utc).isoformat()})
        await asyncio.sleep(2)
