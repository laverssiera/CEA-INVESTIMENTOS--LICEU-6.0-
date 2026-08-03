from __future__ import annotations

import asyncio

from fastapi import FastAPI

from apps.cea.api.finance import router as finance_router
from apps.cea.api.wallet import router as wallet_router
from apps.cea.api.mission import router as mission_router
from apps.cea.consumers.event_consumer import start_consumers
from apps.cea.core.database import Base, engine

app = FastAPI(title="CEA Investimentos")

app.include_router(finance_router)
app.include_router(wallet_router)
app.include_router(mission_router)


@app.on_event("startup")
async def startup() -> None:
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(start_consumers())


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
