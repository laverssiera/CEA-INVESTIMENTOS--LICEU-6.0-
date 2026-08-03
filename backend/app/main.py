from __future__ import annotations

import asyncio
import json
import os
import random
import secrets
from contextlib import asynccontextmanager, suppress
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt
import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException, Request, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.tree import DecisionTreeRegressor
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.events import event_bus
from app.events.bus import start_nats_consumer, stop_nats_consumer
from app.modules.decision_engine import register_trigger_handlers
from app.modules.decision_engine.router import router as decision_engine_router
from app.modules.home_broker.router import investor_router as home_broker_investor_router
from app.modules.home_broker.router import router as home_broker_router
from app.modules.finance_os.router import router as finance_os_router
from app.modules.notifications.router import router as notifications_router
from app.modules.documents.router import router as documents_router
from app.modules.orchestration import OrchestrationScheduler, build_orchestrator
from app.modules.orchestration.router import router as orchestration_router
from app.modules.interplanetary_finance.civilizational_compliance.router import router as compliance_router
from app.modules.interplanetary_finance.scientific_capital.router import router as science_funding_router
from app.modules.interplanetary_finance.planetary_risk.router import router as planetary_risk_router
from app.modules.interplanetary_finance.esg_engine.router import router as civilizational_esg_router
from app.modules.interplanetary_finance.ethical_treasury.router import router as ethical_treasury_router
from app.modules.interplanetary_finance.audit_chain.router import router as audit_chain_router
from app.modules.interplanetary_finance.mission_portfolio.router import router as mission_portfolio_router
from app.routers.interplanetary import router as interplanetary_router
from routers.john_cea import router as john_cea_router
from app.routers.cea_monolith import router as cea_router
from app.cognition.john_gateway import router as cea_cognition_router
from app.routers.finance_runtime import router as finance_runtime_router
from app.routers.cea_governance_router import router as cea_governance_router
from app.routers.runtime_router import router as runtime_router
from app.routers.investments_router import router as investments_router
from backend.app.routers import federation_runtime


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    pix_task = asyncio.create_task(_pix_reconcile_loop())
    scheduler_started = False
    nats_started = False

    try:
        ORCHESTRATION_SCHEDULER.start()
        scheduler_started = True

        await start_nats_consumer()
        nats_started = True

        yield
    finally:
        pix_task.cancel()
        with suppress(asyncio.CancelledError):
            await pix_task

        PIX_RECONCILE_STATE["running"] = False

        if scheduler_started:
            ORCHESTRATION_SCHEDULER.shutdown()
        if nats_started:
            await stop_nats_consumer()

app = FastAPI(
    title="CEA Investimentos API",
    version="2.0.0",
    description="Financial Intelligence Engine integrado à LICEU 6.0 com JWT, MFA e ML",
    lifespan=app_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home_broker_router)
app.include_router(home_broker_investor_router)
app.include_router(finance_os_router)
app.include_router(decision_engine_router)
app.include_router(orchestration_router)
app.include_router(notifications_router)
app.include_router(documents_router)
app.include_router(john_cea_router)
app.include_router(cea_router)
app.include_router(cea_cognition_router)
app.include_router(finance_runtime_router)
app.include_router(cea_governance_router)
app.include_router(compliance_router)
app.include_router(science_funding_router)
app.include_router(planetary_risk_router)
app.include_router(civilizational_esg_router)
app.include_router(ethical_treasury_router)
app.include_router(audit_chain_router)
app.include_router(mission_portfolio_router)
app.include_router(interplanetary_router)
app.include_router(federation_runtime.router)
app.include_router(runtime_router)
app.include_router(investments_router)

ORCHESTRATOR = build_orchestrator()
ORCHESTRATION_SCHEDULER = OrchestrationScheduler(ORCHESTRATOR)
register_trigger_handlers()

SECRET_KEY = os.getenv("CEA_SECRET_KEY", "cea-liceu-6-financial-engine")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_HOURS = 24

BASE_INDICATORS = {
    "cdi": 13.45,
    "selic": 13.75,
    "ipca": 4.31,
    "tesouro_selic": 13.22,
    "ibovespa": 128450,
    "dolar": 5.18,
    "liquidez": "Alta",
}

LICEU_MODULES = {
    "engineering": {
        "endpoint": "/api/engineering/production",
        "produced_m2": 4820,
        "work_progress": 67,
        "productivity": 92,
        "delay_days": 4,
        "milestones": ["Fundação concluída", "Estrutura 82%", "Instalações em andamento"],
    },
    "data": {
        "endpoint": "/api/data/analytics",
        "productivity": 92,
        "cost_efficiency": 88,
        "demand_index": 81,
        "project_risk": "moderado",
    },
    "assets": {
        "endpoint": "/api/assets/projects",
        "projects": 4,
        "landbank_brl": 18500000,
        "valuation_brl": 42600000,
        "active_projects": ["Residencial Alpha", "Lote Beta", "Célula Gama", "Hub Delta"],
    },
    "finance": {
        "endpoint": "/api/finance/cashflow",
        "cash_balance_brl": 12400000,
        "monthly_expenses_brl": 1480000,
        "monthly_income_brl": 2120000,
        "liquidity_buffer_months": 8.4,
    },
    "logistics": {
        "endpoint": "/api/logistics/costs",
        "kit_cost_brl": 128500,
        "supply_chain_status": "estável",
        "lead_time_days": 12,
    },
}

DASHBOARD_SNAPSHOT = {
    "portfolio_value_brl": 28600000,
    "monthly_yield_pct": 1.18,
    "liquidity_label": "Alta",
    "wallet": [
        {"name": "Tesouro Selic", "percentage": 56, "value_brl": 16016000},
        {"name": "CDB 110% CDI", "percentage": 29, "value_brl": 8294000},
        {"name": "Fundo DI", "percentage": 15, "value_brl": 4290000},
    ],
    "performance_series": [0.72, 0.81, 0.95, 1.03, 1.11, 1.18],
    "active_projects": [
        {"name": "Residencial Alpha", "status": "Captação", "progress": 67},
        {"name": "Lote Beta", "status": "Execução", "progress": 54},
        {"name": "Hub Delta", "status": "Pré-operação", "progress": 31},
    ],
}

SECURITY_POSTURE = {
    "network": ["TLS 1.3", "WAF", "Rate limiting", "Proteção DDoS"],
    "identity": ["OAuth2", "JWT curto", "Refresh token", "MFA obrigatório"],
    "data": ["AES-256 at-rest", "CSP", "CSRF token", "Logs imutáveis"],
    "governance": ["RBAC", "Zero Trust", "IP allowlist", "Auditoria contínua"],
}

ALERTS = [
    {"level": "warning", "title": "SELIC em alta", "message": "Ajustar duration para preservar liquidez das obras."},
    {"level": "info", "title": "Oportunidade renda fixa", "message": "CDB 110% CDI apresenta prêmio acima do benchmark."},
    {"level": "critical", "title": "Rebalanceamento sugerido", "message": "Fluxo de caixa da frente B pede 8% adicional em caixa imediato."},
]

DEMO_USERS = {
    "investidor": {
        "password": "cea123",
        "role": "investor_pf",
        "full_name": "Investidor Demo",
        "mfa_code": "246810",
    },
    "investor_pj": {
        "password": "cea123",
        "role": "investor_pj",
        "full_name": "Investidor PJ Demo",
        "mfa_code": "246810",
    },
    "cliente": {
        "password": "cliente123",
        "role": "cliente_financiamento",
        "full_name": "Cliente Financiamento Demo",
        "mfa_code": "112233",
    },
    "admin": {
        "password": "admin123",
        "role": "admin",
        "full_name": "Administrador Demo",
        "mfa_code": "999000",
    },
    "analista_credito": {
        "password": "credito123",
        "role": "analista_credito",
        "full_name": "Analista de Credito Demo",
        "mfa_code": "224466",
    },
    "compliance": {
        "password": "compliance123",
        "role": "compliance",
        "full_name": "Compliance Demo",
        "mfa_code": "778899",
    },
    "tesouraria": {
        "password": "tesouraria123",
        "role": "tesouraria",
        "full_name": "Tesouraria Demo",
        "mfa_code": "554433",
    },
    "colaborador": {
        "password": "colaborador123",
        "role": "colaborador",
        "full_name": "Colaborador Interno Demo",
        "mfa_code": "667788",
    },
    "risk_manager": {
        "password": "risk123",
        "role": "risk_manager",
        "full_name": "Risk Manager Demo",
        "mfa_code": "313131",
    },
    "governance": {
        "password": "gov123",
        "role": "governance",
        "full_name": "Governance Officer Demo",
        "mfa_code": "414141",
    },
    "diretoria": {
        "password": "board123",
        "role": "diretoria",
        "full_name": "Diretoria Demo",
        "mfa_code": "515151",
    },
    "operador": {
        "password": "liceu123",
        "role": "admin",
        "full_name": "Operador LICEU",
        "mfa_code": "135790",
    },
}

MFA_CHALLENGES: dict[str, dict] = {}

INVESTOR_ROLES = {"investor_pf", "investor_pj"}
COLLABORATOR_ROLES = {"analista_credito", "compliance", "tesouraria", "colaborador"}
BACKOFFICE_ROLES = {"admin", "risk_manager", "governance", "diretoria"}
STAFF_ROLES = COLLABORATOR_ROLES | BACKOFFICE_ROLES
ALL_ROLES = INVESTOR_ROLES | STAFF_ROLES | {"cliente_financiamento"}

PIX_RBAC_ACTIONS: dict[str, set[str]] = {
    "pix.reconcile": {"admin", "tesouraria", "risk_manager", "governance"},
    "pix.audit": {"admin", "compliance", "risk_manager", "governance"},
    "pix.kpis": {"admin", "tesouraria", "risk_manager", "governance"},
    "pix.withdraw.approve": {"admin", "tesouraria", "risk_manager"},
}

INVESTOR_ONBOARDINGS: dict[str, dict[str, Any]] = {
    "investidor": {
        "status": "approved",
        "profile": "investor_pf",
        "cpf": "12345678900",
        "address": "Sao Paulo/SP",
        "income_brl": 45000,
        "patrimony_brl": 1200000,
        "origin_of_funds": "renda profissional",
        "suitability": "moderado",
    },
    "investor_pj": {
        "status": "approved",
        "profile": "investor_pj",
        "cpf": "12345678000199",
        "address": "Campinas/SP",
        "income_brl": 320000,
        "patrimony_brl": 8500000,
        "origin_of_funds": "fluxo operacional",
        "suitability": "arrojado",
    },
}

INVESTMENT_PRODUCTS: dict[str, dict[str, Any]] = {
    "PROD-LICEU-RF-01": {
        "id": "PROD-LICEU-RF-01",
        "name": "Renda Fixa Imobiliaria LICEU",
        "yield": 0.16,
        "duration_months": 18,
        "min_investment": 5000,
        "max_per_investor": 400000,
        "total_cap_limit": 3000000,
        "allocated_total": 0.0,
        "status": "open",
        "project_risk": "medio",
    }
}

INVESTMENT_ORDERS: list[dict[str, Any]] = []
INVESTMENT_POSITIONS: dict[str, dict[str, Any]] = {}

FINANCING_REQUESTS: dict[str, dict[str, Any]] = {}
FINANCING_PIPELINE = ["submitted", "under_review", "approved", "funded", "in_execution", "closed"]

TREASURY_TRANSACTIONS: list[dict[str, Any]] = []
AUDIT_LOGS: list[dict[str, Any]] = []

LICEU_PROJECTS: dict[str, dict[str, Any]] = {
    "alpha": {"id": "alpha", "name": "Residencial Alpha", "progress": 35, "stage": "estrutura", "risk": "baixo"},
    "beta": {"id": "beta", "name": "Lote Beta", "progress": 54, "stage": "instalacoes", "risk": "medio"},
}

JOB_REGISTRY = {
    "market_update": "Atualiza indicadores de mercado e parâmetros de alocação.",
    "portfolio_risk_score": "Calcula score consolidado de risco da carteira.",
    "liquidity_alerts": "Processa alertas e concentração de liquidez operacional.",
    "liceu_projects_update": "Sincroniza progresso de projetos LICEU.",
    "daily_operation_report": "Consolida relatório diário institucional.",
}

JOB_SCHEDULES = [
    {
        "name": "market_update",
        "schedule": "08:00",
        "description": "Atualização de mercado.",
    },
    {
        "name": "portfolio_risk_score",
        "schedule": "09:00",
        "description": "Score de risco da carteira.",
    },
    {
        "name": "liquidity_alerts",
        "schedule": "12:00",
        "description": "Alertas de liquidez.",
    },
    {
        "name": "liceu_projects_update",
        "schedule": "15:00",
        "description": "Atualização de projetos LICEU.",
    },
    {
        "name": "daily_operation_report",
        "schedule": "18:00",
        "description": "Relatório diário institucional.",
    },
]

COMMITTEES = [
    "Comitê de Crédito",
    "Comitê de Investimentos",
    "Comitê ESG",
    "Comitê de Risco",
    "Comitê de Liquidez",
]

COMMITTEE_DECISIONS: list[dict[str, Any]] = [
    {
        "id": "CD-001",
        "committee": "Comitê de Crédito",
        "date": "2026-03-12",
        "participants": ["analista_credito", "tesouraria", "compliance"],
        "decision": "Aprovado",
        "approved_amount": 18000000.0,
        "risk_notes": "Tranche 1: 8M | Tranche 2: 10M após 40% da obra",
    }
]

OPERATIONS_ROUTINES = [
    {
        "area": "Crédito e comitê",
        "window": "09:00-11:00",
        "focus": "Conferência documental, parecer técnico e pré-comitê.",
    },
    {
        "area": "Tesouraria",
        "window": "11:00-12:00",
        "focus": "Posição de caixa, funding e necessidade de liquidez imediata.",
    },
    {
        "area": "Compliance",
        "window": "14:00-15:00",
        "focus": "KYC pendente, AML, suitability e segregação de funções.",
    },
    {
        "area": "Governança",
        "window": "17:30-18:00",
        "focus": "Fechamento executivo, auditoria e atualização de indicadores.",
    },
]

ESG_CALENDAR = [
    {
        "period": "Mensal",
        "title": "Reporte de governance ESG",
        "description": "Consolidação de pendências, ritos de comitê e evolução de planos de ação.",
    },
    {
        "period": "Trimestral",
        "title": "Comitê integrado de risco e ESG",
        "description": "Revisão de materialidade, apetite a risco e indicadores de obras e fornecedores.",
    },
    {
        "period": "Semestral",
        "title": "Teste de controles e acessos",
        "description": "Validação da matriz RBAC, segregação crítica e trilha de aprovação dupla.",
    },
]

CREDIT_COMMITTEE_MEMBERS = [
    {"name": "Diretoria Executiva", "role": "Presidência do comitê", "vote": "Voto final"},
    {"name": "Risk Manager", "role": "Parecer de risco", "vote": "Obrigatório"},
    {"name": "Governance Officer", "role": "Segregação e rito", "vote": "Obrigatório"},
    {"name": "Analista de Crédito", "role": "Relator técnico", "vote": "Consultivo"},
]

CREDIT_COMMITTEE_RULES = [
    "Operações acima de R$ 5 mi exigem aprovação dupla entre diretoria e risk manager.",
    "Nenhum originador pode aprovar a própria operação.",
    "Compliance valida dossiê completo antes da pauta deliberativa.",
    "Status funded depende de liberação formal da tesouraria.",
]

RBAC_TECHNICAL_RULES = [
    "Perfis de governança possuem leitura global e aprovação restrita por escopo.",
    "Tesouraria não aprova crédito, apenas executa funding após deliberação formal.",
    "Compliance mantém veto operacional em KYC, AML e suitability.",
    "Módulos críticos exigem MFA e trilha de auditoria persistente.",
]

ML_TRAINING_FRAME = pd.DataFrame(
    [
        {"project_term_days": 15, "interest_rate": 13.25, "cash_balance_mil": 6.0, "risk_index": 22, "expected_yield": 0.48},
        {"project_term_days": 30, "interest_rate": 13.50, "cash_balance_mil": 12.0, "risk_index": 28, "expected_yield": 0.62},
        {"project_term_days": 45, "interest_rate": 13.75, "cash_balance_mil": 12.4, "risk_index": 35, "expected_yield": 0.82},
        {"project_term_days": 60, "interest_rate": 13.80, "cash_balance_mil": 16.0, "risk_index": 42, "expected_yield": 0.96},
        {"project_term_days": 90, "interest_rate": 13.95, "cash_balance_mil": 18.0, "risk_index": 48, "expected_yield": 1.08},
        {"project_term_days": 120, "interest_rate": 14.10, "cash_balance_mil": 20.0, "risk_index": 54, "expected_yield": 1.24},
        {"project_term_days": 180, "interest_rate": 14.20, "cash_balance_mil": 24.0, "risk_index": 62, "expected_yield": 1.38},
    ]
)

ML_MODEL = DecisionTreeRegressor(max_depth=4, random_state=42)
ML_MODEL.fit(
    ML_TRAINING_FRAME[["project_term_days", "interest_rate", "cash_balance_mil", "risk_index"]],
    ML_TRAINING_FRAME["expected_yield"],
)


class SimulationInput(BaseModel):
    cash_balance: float = Field(gt=0, description="Saldo disponível para alocação")
    project_horizon_days: int = Field(gt=0, le=720)
    liquidity_need: Literal["alta", "média", "baixa"]
    risk_profile: Literal["baixo", "moderado", "alto"]


class RecommendationPayload(SimulationInput):
    pass


class LoginInput(BaseModel):
    username: str
    password: str


class RefreshInput(BaseModel):
    refresh_token: str


class MfaVerifyInput(BaseModel):
    challenge_id: str
    code: str = Field(min_length=6, max_length=6)


class CreditScoreInput(BaseModel):
    investment_history: float = Field(default=85, ge=0, le=100)
    liquidity_work: float = Field(default=88, ge=0, le=100)
    engineering_productivity: float = Field(default=92, ge=0, le=100)
    project_risk: float = Field(default=20, ge=0, le=100)
    project_term_days: int = Field(default=45, ge=1, le=360)


class ComplianceInput(BaseModel):
    investor_name: str = "Investidor Demo"
    investment_amount: float = Field(default=250000, gt=0)
    kyc_completed: bool = True
    aml_flag: bool = False
    suitability_profile: Literal["conservador", "moderado", "arrojado"] = "moderado"


class MLDecisionInput(BaseModel):
    project_term_days: int = Field(default=45, ge=1, le=360)
    interest_rate: float = Field(default=13.75, ge=0, le=30)
    cash_balance: float = Field(default=12400000, gt=0)
    risk_index: float = Field(default=35, ge=0, le=100)


class InvestorSignupInput(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=80)
    full_name: str = Field(min_length=3, max_length=120)
    profile: Literal["investor_pf", "investor_pj"] = "investor_pf"


class InvestorKYCInput(BaseModel):
    cpf: str = Field(min_length=11, max_length=18)
    address: str = Field(min_length=4, max_length=180)
    income_brl: float = Field(gt=0)
    patrimony_brl: float = Field(gt=0)
    origin_of_funds: str = Field(min_length=3, max_length=180)


class InvestorSuitabilityInput(BaseModel):
    answers: list[int] = Field(min_length=4, max_length=20)


class InvestmentProductInput(BaseModel):
    name: str = Field(min_length=4, max_length=120)
    yield_value: float = Field(alias="yield", gt=0, le=1)
    duration_months: int = Field(gt=0, le=360)
    min_investment: float = Field(gt=0)
    max_per_investor: float = Field(gt=0)
    total_cap_limit: float = Field(gt=0)
    project_risk: Literal["baixo", "medio", "alto"] = "medio"


class InvestmentOrderInput(BaseModel):
    product_id: str
    amount: float = Field(gt=0)


class FinancingStatusInput(BaseModel):
    status: Literal["submitted", "under_review", "approved", "funded", "in_execution", "closed"]


class TreasuryTransactionInput(BaseModel):
    type: Literal["investor_inflow", "financing_outflow", "adjustment"]
    amount: float = Field(gt=0)
    source: str = Field(min_length=2, max_length=120)
    destination: str = Field(min_length=2, max_length=120)
    status: Literal["pending", "completed", "failed"] = "pending"


class CommitteeDecisionInput(BaseModel):
    committee: Literal[
        "Comitê de Crédito",
        "Comitê de Investimentos",
        "Comitê ESG",
        "Comitê de Risco",
        "Comitê de Liquidez",
    ]
    date: str = Field(min_length=10, max_length=30)
    participants: list[str] = Field(min_length=1)
    decision: str = Field(min_length=2, max_length=120)
    approved_amount: float = Field(ge=0)
    risk_notes: str = Field(min_length=2, max_length=500)


def create_jwt_token(subject: str, role: str, expires_delta: timedelta, token_type: str = "access") -> str:
    issued_at = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "role": role,
        "type": token_type,
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + expires_delta).timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_token(token: str, expected_type: str | None = None) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido") from exc

    if expected_type and payload.get("type") != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tipo de token inválido")
    return payload


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token obrigatório")

    token = authorization.split(" ", 1)[1]
    payload = decode_jwt_token(token, expected_type="access")
    username = payload.get("sub")
    user = DEMO_USERS.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")

    return {"username": username, **user}


def audit_log(action: str, user: dict, payload: dict | None = None) -> None:
    AUDIT_LOGS.append(
        {
            "id": secrets.token_hex(6),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "username": user["username"],
            "role": user["role"],
            "payload": payload or {},
        }
    )


def require_role(role: str):
    def wrapper(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissao")
        return user

    return wrapper


def require_any_role(roles: set[str]):
    def wrapper(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissao")
        return user

    return wrapper


def require_pix_action(action: str, user: dict) -> None:
    allowed = PIX_RBAC_ACTIONS.get(action, set())
    if allowed and user.get("role") not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Sem permissao para {action}")


def resolve_investor_limits(product: dict[str, Any]) -> dict[str, float]:
    # Regra da camada 9: projeto de risco alto restringe captacao PF em 30%
    max_pf_allocation = 0.3 if product.get("project_risk") == "alto" else 0.7
    return {
        "max_pf_allocation": max_pf_allocation,
        "max_pf_value": round(product["total_cap_limit"] * max_pf_allocation, 2),
    }


def can_invest(username: str) -> bool:
    onboarding = INVESTOR_ONBOARDINGS.get(username)
    return bool(onboarding and onboarding.get("status") == "approved")


def build_recommendation(payload: SimulationInput) -> dict:
    horizon = payload.project_horizon_days
    liquidity = payload.liquidity_need
    risk = payload.risk_profile

    if horizon < 30 or liquidity == "alta":
        allocation = [
            {"asset": "Tesouro Selic", "percentage": 60},
            {"asset": "CDB 110% CDI", "percentage": 30},
            {"asset": "Fundo DI", "percentage": 10},
        ]
        risk_level = "baixo"
        estimated_return = "CDI + 0.4%"
    elif horizon <= 90 and risk != "alto":
        allocation = [
            {"asset": "CDB liquidez diária", "percentage": 45},
            {"asset": "Tesouro Selic", "percentage": 35},
            {"asset": "Debêntures incentivadas", "percentage": 20},
        ]
        risk_level = "moderado"
        estimated_return = "CDI + 0.9%"
    else:
        allocation = [
            {"asset": "Fundo DI", "percentage": 30},
            {"asset": "Debêntures high grade", "percentage": 40},
            {"asset": "Tesouro IPCA+", "percentage": 30},
        ]
        risk_level = "moderado-alto" if risk == "alto" else "moderado"
        estimated_return = "IPCA + 6.2%"

    projected_income = round(payload.cash_balance * (0.0045 if risk_level == "baixo" else 0.0075), 2)

    return {
        "allocation": allocation,
        "risk_level": risk_level,
        "expected_return": estimated_return,
        "projected_monthly_income_brl": projected_income,
        "rationale": [
            f"Horizonte da obra: {horizon} dias",
            f"Necessidade de liquidez: {liquidity}",
            f"Perfil de risco: {risk}",
        ],
    }


def calculate_credit_engine(payload: CreditScoreInput) -> dict:
    term_component = max(0, 100 - min(100, payload.project_term_days / 1.8))
    risk_component = max(0, 100 - payload.project_risk)

    weighted_score = (
        0.3 * payload.engineering_productivity
        + 0.2 * payload.liquidity_work
        + 0.2 * payload.investment_history
        + 0.15 * term_component
        + 0.15 * risk_component
    )
    score = int(max(450, min(850, round(360 + weighted_score * 5.4))))

    if score >= 780:
        risk = "LOW"
        allocation = "TREASURY_SELIC"
    elif score >= 680:
        risk = "MEDIUM"
        allocation = "CDB_LIQUIDEZ"
    else:
        risk = "HIGH"
        allocation = "FUNDO_DI"

    return {
        "score": score,
        "risk": risk,
        "recommended_allocation": allocation,
        "breakdown": {
            "productivity": payload.engineering_productivity,
            "liquidity": payload.liquidity_work,
            "investment_history": payload.investment_history,
            "project_term": term_component,
            "risk": risk_component,
        },
    }


def build_governance_audit_trail() -> list[dict[str, str]]:
    recent_logs = AUDIT_LOGS[-4:]
    if recent_logs:
        return [
            {
                "timestamp": item["timestamp"],
                "action": item["action"],
                "user": item["username"],
                "module": item.get("payload", {}).get("job_name") or item.get("payload", {}).get("request_id") or "operacoes",
            }
            for item in reversed(recent_logs)
        ]

    return [
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "governance.snapshot_refreshed",
            "user": "system",
            "module": "governanca",
        },
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "credit.committee_precheck",
            "user": "analista_credito",
            "module": "credito",
        },
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "compliance.access_review",
            "user": "compliance",
            "module": "compliance",
        },
    ]


def build_committee_queue() -> list[dict[str, Any]]:
    queue = []
    for item in FINANCING_REQUESTS.values():
        queue.append(
            {
                "project": item["company_name"],
                "value": f"R$ {item['requested_amount']:,.0f}".replace(",", "."),
                "status": item["status"],
                "double_approval": item["requested_amount"] >= 5000000,
            }
        )

    if queue:
        return queue[:6]

    return [
        {"project": "Residencial Alpha", "value": "R$ 6.800.000", "status": "under_review", "double_approval": True},
        {"project": "Lote Beta", "value": "R$ 3.200.000", "status": "approved", "double_approval": False},
        {"project": "Hub Delta", "value": "R$ 8.100.000", "status": "submitted", "double_approval": True},
    ]


def build_risk_engine() -> dict:
    total_requests = sum(item["requested_value"] for item in FINANCING_REQUESTS.values())
    total_allocated = sum(item.get("allocated_total", 0.0) for item in INVESTMENT_PRODUCTS.values())
    base_portfolio = total_requests + total_allocated
    carteira_ativa = base_portfolio if base_portfolio > 0 else 210000000.0

    by_project = []
    for project in LICEU_PROJECTS.values():
        exposure = round(carteira_ativa * (project["progress"] / 100) * 0.12, 2)
        by_project.append(
            {
                "project": project["name"],
                "exposure": exposure,
                "share": round((exposure / carteira_ativa) * 100, 2),
            }
        )

    by_client = []
    for item in list(FINANCING_REQUESTS.values())[:8]:
        exposure = item["requested_value"]
        by_client.append(
            {
                "client": item["client_name"],
                "exposure": exposure,
                "share": round((exposure / carteira_ativa) * 100, 2),
            }
        )

    if not by_client:
        by_client = [
            {"client": "Residencial Alpha SPE", "exposure": 31500000.0, "share": 15.0},
            {"client": "Lote Beta SPE", "exposure": 25200000.0, "share": 12.0},
            {"client": "Hub Delta SPE", "exposure": 21000000.0, "share": 10.0},
        ]

    concentration = max([item["share"] for item in by_project], default=0.0)
    client_exposure = max([item["share"] for item in by_client], default=0.0)
    entries = sum(t["amount"] for t in TREASURY_TRANSACTIONS if t["type"] == "investor_inflow")
    outflows = sum(t["amount"] for t in TREASURY_TRANSACTIONS if t["type"] == "financing_outflow")
    liquidity_available = round(entries - outflows, 2) if entries or outflows else 48000000.0
    var_simplified = round(carteira_ativa * 0.021, 2)

    return {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "exposure_by_project": by_project,
        "exposure_by_client": by_client,
        "portfolio_concentration": round(concentration, 2),
        "available_liquidity": liquidity_available,
        "var_simplified": var_simplified,
        "kpis": {
            "max_concentration_limit": 25.0,
            "client_exposure_limit": 15.0,
            "portfolio_concentration": round(concentration, 2),
            "client_max_exposure": round(client_exposure, 2),
            "avg_ltv_portfolio": 62.0,
            "funding_duration_months": 18.0,
        },
    }


def build_daily_operation_report() -> dict:
    return {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "captacao_total": 92000000.0,
        "credito_aprovado": 41000000.0,
        "carteira_ativa": 210000000.0,
        "roi_medio_pct": 14.2,
        "esg_score_medio": 78,
        "alerts": [
            "concentração SP: 28%",
            "funding curto prazo: atenção",
        ],
    }


def run_decision_tree(payload: MLDecisionInput) -> dict:
    features = pd.DataFrame(
        [
            {
                "project_term_days": payload.project_term_days,
                "interest_rate": payload.interest_rate,
                "cash_balance_mil": payload.cash_balance / 1_000_000,
                "risk_index": payload.risk_index,
            }
        ]
    )

    expected_yield = float(
        ML_MODEL.predict(features[["project_term_days", "interest_rate", "cash_balance_mil", "risk_index"]])[0]
    )

    if payload.risk_index >= 65 or payload.project_term_days < 30:
        allocation = "TREASURY_SELIC"
    elif payload.project_term_days <= 90:
        allocation = "CDB_110_CDI"
    else:
        allocation = "FUNDO_DI"

    confidence = float(np.clip(0.93 - (payload.risk_index / 250) + (payload.cash_balance / 120_000_000), 0.7, 0.97))

    return {
        "allocation": allocation,
        "expected_yield": round(expected_yield, 2),
        "confidence": round(confidence, 2),
        "model": "DecisionTreeRegressor",
    }


@app.post("/auth/login")
def auth_login(payload: LoginInput) -> dict:
    user = DEMO_USERS.get(payload.username)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    challenge_id = secrets.token_hex(8)
    MFA_CHALLENGES[challenge_id] = {
        "username": payload.username,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5),
        "code": user["mfa_code"],
    }

    temporary_token = create_jwt_token(payload.username, user["role"], timedelta(minutes=5), token_type="pre_mfa")
    audit_log("auth.login_challenge", {"username": payload.username, **user})
    return {
        "mfa_required": True,
        "challenge_id": challenge_id,
        "temporary_token": temporary_token,
        "user_role": user["role"],
        "otp_hint": f"Código demo: {user['mfa_code']}",
    }


@app.post("/auth/mfa/verify")
def verify_mfa(payload: MfaVerifyInput) -> dict:
    challenge = MFA_CHALLENGES.get(payload.challenge_id)
    if not challenge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge MFA não encontrado")

    if challenge["expires_at"] < datetime.now(timezone.utc):
        MFA_CHALLENGES.pop(payload.challenge_id, None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Challenge MFA expirado")

    if challenge["code"] != payload.code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código MFA inválido")

    username = challenge["username"]
    user = DEMO_USERS[username]
    MFA_CHALLENGES.pop(payload.challenge_id, None)

    access_token = create_jwt_token(username, user["role"], timedelta(minutes=ACCESS_TOKEN_MINUTES))
    refresh_token = create_jwt_token(username, user["role"], timedelta(hours=REFRESH_TOKEN_HOURS), token_type="refresh")

    audit_log("auth.mfa_verified", {"username": username, **user})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_MINUTES * 60,
        "role": user["role"],
        "user": {"name": user["full_name"], "username": username},
    }


@app.post("/auth/refresh")
def refresh_token(payload: RefreshInput) -> dict:
    token_payload = decode_jwt_token(payload.refresh_token, expected_type="refresh")
    username = token_payload.get("sub")
    user = DEMO_USERS.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")

    access_token = create_jwt_token(username, user["role"], timedelta(minutes=ACCESS_TOKEN_MINUTES))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_MINUTES * 60,
    }


@app.post("/api/investor/signup", status_code=status.HTTP_201_CREATED)
def investor_signup(payload: InvestorSignupInput) -> dict:
    if payload.username in DEMO_USERS:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuario ja existe")

    DEMO_USERS[payload.username] = {
        "password": payload.password,
        "role": payload.profile,
        "full_name": payload.full_name,
        "mfa_code": "246810",
    }
    INVESTOR_ONBOARDINGS[payload.username] = {
        "status": "pending",
        "profile": payload.profile,
        "cpf": "",
        "address": "",
        "income_brl": 0,
        "patrimony_brl": 0,
        "origin_of_funds": "",
        "suitability": "nao_definido",
    }
    return {"status": "pending", "username": payload.username, "next": "Enviar KYC"}


@app.post("/api/investor/kyc")
def investor_kyc(payload: InvestorKYCInput, user: dict = Depends(require_any_role(INVESTOR_ROLES))) -> dict:
    onboarding = INVESTOR_ONBOARDINGS.setdefault(user["username"], {"status": "pending", "profile": user["role"]})
    onboarding.update(payload.model_dump())
    onboarding["status"] = "pending"
    event_bus.publish("investor.kyc_pending", {"username": user["username"], "profile": user["role"]})
    audit_log("investor.kyc_submitted", user, payload.model_dump())
    return {"status": onboarding["status"], "message": "KYC recebido para analise"}


@app.post("/api/investor/suitability")
def investor_suitability(payload: InvestorSuitabilityInput, user: dict = Depends(require_any_role(INVESTOR_ROLES))) -> dict:
    score = sum(payload.answers)
    profile = "conservador" if score <= 20 else "moderado" if score <= 35 else "arrojado"
    onboarding = INVESTOR_ONBOARDINGS.setdefault(user["username"], {"status": "pending", "profile": user["role"]})
    onboarding["suitability"] = profile
    onboarding["status"] = "approved" if onboarding.get("cpf") else "pending"
    audit_log("investor.suitability_done", user, {"score": score, "profile": profile})
    return {"status": onboarding["status"], "suitability": profile}


@app.get("/api/investor/onboarding")
def investor_onboarding(user: dict = Depends(require_any_role(INVESTOR_ROLES))) -> dict:
    data = INVESTOR_ONBOARDINGS.get(user["username"], {"status": "pending", "profile": user["role"]})
    return {"username": user["username"], **data}


@app.post("/api/investments/products", status_code=status.HTTP_201_CREATED)
def create_product(payload: InvestmentProductInput, user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    if user["role"] not in {"admin", "tesouraria", "compliance"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissao para criar produto")

    product_id = f"PROD-{secrets.token_hex(4).upper()}"
    item = {
        "id": product_id,
        "name": payload.name,
        "yield": payload.yield_value,
        "duration_months": payload.duration_months,
        "min_investment": payload.min_investment,
        "max_per_investor": payload.max_per_investor,
        "total_cap_limit": payload.total_cap_limit,
        "allocated_total": 0.0,
        "status": "open",
        "project_risk": payload.project_risk,
    }
    INVESTMENT_PRODUCTS[product_id] = item
    audit_log("investments.product_created", user, {"product_id": product_id})
    return item


@app.get("/api/investments/products")
def list_products(user: dict = Depends(get_current_user)) -> dict:
    visible = []
    for product in INVESTMENT_PRODUCTS.values():
        limits = resolve_investor_limits(product)
        visible.append({**product, "allocation_rules": limits})

    # Investidor nao ve dados de credito internos
    return {"items": visible, "role": user["role"]}


@app.post("/api/investments/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: InvestmentOrderInput, user: dict = Depends(require_any_role(INVESTOR_ROLES))) -> dict:
    product = INVESTMENT_PRODUCTS.get(payload.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado")
    if product["status"] != "open":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto fechado")
    if not can_invest(user["username"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Onboarding pendente. Nao pode investir")
    if payload.amount < product["min_investment"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aporte abaixo do minimo")
    if payload.amount > product["max_per_investor"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aporte acima do limite por investidor")

    new_allocated = product["allocated_total"] + payload.amount
    if new_allocated > product["total_cap_limit"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limite total de captacao atingido")

    rules = resolve_investor_limits(product)
    if user["role"] == "investor_pf" and new_allocated > rules["max_pf_value"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limite PF para este projeto atingido")

    wallet = _get_wallet(user["username"])
    if wallet["balance"] < payload.amount:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Saldo insuficiente na wallet interna")

    # Bloqueio de saldo: reduz disponivel e aumenta bloqueado
    wallet["balance"] = round(wallet["balance"] - payload.amount, 2)
    wallet["locked"] = round(wallet.get("locked", 0.0) + payload.amount, 2)
    wallet["updated_at"] = datetime.now(timezone.utc).isoformat()

    product["allocated_total"] = new_allocated
    if product["allocated_total"] >= product["total_cap_limit"]:
        product["status"] = "closed"

    order = {
        "id": f"ORD-{secrets.token_hex(5).upper()}",
        "investor": user["username"],
        "product_id": payload.product_id,
        "amount": payload.amount,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    INVESTMENT_ORDERS.append(order)

    position = INVESTMENT_POSITIONS.setdefault(user["username"], {"total_invested": 0.0, "orders": []})
    position["total_invested"] += payload.amount
    position["orders"].append(order["id"])
    event_bus.publish(
        "investment.created",
        {
            "order_id": order["id"],
            "amount": payload.amount,
            "profile": "moderado",
            "risk": 55,
        },
    )
    _new_ledger_entry(user["username"], "investimento", payload.amount, order["id"])
    audit_log("investments.order_created", user, {"order_id": order["id"], "amount": payload.amount})
    return order


@app.get("/api/investments/positions")
def list_positions(user: dict = Depends(require_any_role(INVESTOR_ROLES))) -> dict:
    return INVESTMENT_POSITIONS.get(user["username"], {"total_invested": 0.0, "orders": []})


@app.get("/health")
def healthcheck() -> dict:
    return {
        "status": "ok",
        "service": "cea-api",
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/contact")
def get_contact_info() -> dict:
    return {
        "phone": "+55 11 4000-0000",
        "whatsapp": "+55 11 90000-0000",
        "email": "atendimento@ceainvestimentos.com",
        "hours": "09:00-18:00",
        "days": "Segunda a sexta",
        "address": "Av. Paulista, 1000 — São Paulo/SP",
    }


@app.get("/api/system/persistence-status")
def persistence_status(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {
            "database": "connected",
            "engine": "postgresql",
            "migration_tool": "alembic",
            "mode": "persistent",
        }
    except Exception:
        return {
            "database": "unavailable",
            "engine": "postgresql",
            "migration_tool": "alembic",
            "mode": "fallback_in_memory",
        }


@app.get("/api/market/indicators")
def market_indicators() -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "indicators": BASE_INDICATORS,
        "yield_curve": [12.9, 13.1, 13.35, 13.48, 13.62],
    }


@app.get("/api/market/alerts")
def market_alerts() -> dict:
    return {"items": ALERTS}


@app.get("/api/market/recommendation")
def default_recommendation() -> dict:
    return build_recommendation(
        SimulationInput(
            cash_balance=12400000,
            project_horizon_days=45,
            liquidity_need="alta",
            risk_profile="baixo",
        )
    )


@app.post("/api/market/simulate")
def simulate_allocation(payload: RecommendationPayload) -> dict:
    return build_recommendation(payload)


@app.get("/api/engineering/production")
def engineering_production() -> dict:
    return LICEU_MODULES["engineering"]


@app.get("/api/data/analytics")
def data_analytics() -> dict:
    return LICEU_MODULES["data"]


@app.get("/api/assets/projects")
def assets_projects() -> dict:
    return LICEU_MODULES["assets"]


@app.get("/api/finance/cashflow")
def finance_cashflow() -> dict:
    return LICEU_MODULES["finance"]


@app.get("/api/logistics/costs")
def logistics_costs() -> dict:
    return LICEU_MODULES["logistics"]


@app.get("/api/liceu/overview")
def liceu_overview() -> dict:
    return LICEU_MODULES


@app.get("/api/security/posture")
def security_posture() -> dict:
    return SECURITY_POSTURE


@app.get("/api/dashboard/portfolio")
def dashboard_portfolio(user: dict = Depends(get_current_user)) -> dict:
    return {
        **DASHBOARD_SNAPSHOT,
        "user": {"name": user["full_name"], "role": user["role"]},
    }


@app.get("/api/credit/score")
def credit_score_preview(_: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    return calculate_credit_engine(CreditScoreInput())


@app.post("/api/credit/score")
def credit_score(payload: CreditScoreInput, _: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    return calculate_credit_engine(payload)


@app.post("/api/compliance/check")
def compliance_check(payload: ComplianceInput, _: dict = Depends(require_any_role({"compliance", "admin"}))) -> dict:
    issues: list[str] = []

    if not payload.kyc_completed:
        issues.append("KYC pendente")
    if payload.aml_flag:
        issues.append("Alerta PLD/AML")
    if payload.suitability_profile == "conservador" and payload.investment_amount > 300000:
        issues.append("Valor acima do limite para perfil conservador")

    return {
        "status": "APPROVED" if not issues else "REVIEW",
        "checks": {
            "kyc": payload.kyc_completed,
            "aml": not payload.aml_flag,
            "suitability": payload.suitability_profile,
        },
        "issues": issues,
    }


class FinancingRequestInput(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    cpf_cnpj: str = Field(min_length=11, max_length=18)
    email: str = Field(min_length=5, max_length=120)
    has_land: bool
    location: str = Field(min_length=3, max_length=120)
    project_type: str = Field(min_length=3, max_length=80)
    requested_value: float = Field(gt=0)
    term_months: int = Field(gt=0, le=360)


class CareerApplicationInput(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    email: str = Field(min_length=5, max_length=120)
    area: str = Field(min_length=2, max_length=80)
    linkedin: str = Field(default='', max_length=200)
    message: str = Field(default='', max_length=800)


class SupportTicketInput(BaseModel):
    subject: str = Field(min_length=4, max_length=160)
    message: str = Field(min_length=10, max_length=1200)
    email: str = Field(default='', max_length=120)


@app.post("/api/financing/request", status_code=status.HTTP_201_CREATED)
def financing_request(payload: FinancingRequestInput) -> dict:
    request_id = secrets.token_hex(6).upper()
    FINANCING_REQUESTS[request_id] = {
        "id": request_id,
        "client_name": payload.name,
        "cpf_cnpj": payload.cpf_cnpj,
        "email": payload.email,
        "has_land": payload.has_land,
        "location": payload.location,
        "project_type": payload.project_type,
        "requested_value": payload.requested_value,
        "term_months": payload.term_months,
        "status": "submitted",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    event_bus.publish("credit.requested", {"request_id": request_id, "requested_value": payload.requested_value})
    return {
        "id": request_id,
        "status": "submitted",
        "message": "Solicitação recebida. O time de crédito entrará em contato em até 2 dias úteis.",
        "data": {
            "name": payload.name,
            "email": payload.email,
            "location": payload.location,
            "project_type": payload.project_type,
            "requested_value": payload.requested_value,
            "term_months": payload.term_months,
            "has_land": payload.has_land,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/credit/requests")
def list_credit_requests(user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    audit_log("credit.requests_listed", user)
    return {"items": list(FINANCING_REQUESTS.values())}


@app.post("/api/credit/requests/{request_id}/status")
def update_credit_request_status(
    request_id: str,
    payload: FinancingStatusInput,
    user: dict = Depends(require_any_role(STAFF_ROLES)),
) -> dict:
    item = FINANCING_REQUESTS.get(request_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitacao nao encontrada")
    if payload.status not in FINANCING_PIPELINE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status invalido")

    if payload.status == "approved" and user["role"] != "analista_credito":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Somente analista_credito aprova")
    if payload.status == "funded" and user["role"] != "tesouraria":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Somente tesouraria libera fundos")

    item["status"] = payload.status
    item["updated_at"] = datetime.now(timezone.utc).isoformat()
    if payload.status == "approved":
        event_bus.publish("credit.approved", {"request_id": request_id, "approved_by": user["username"]})
    audit_log("credit.request_status_updated", user, {"request_id": request_id, "status": payload.status})
    return item


@app.get("/investor/dashboard")
def investor_dashboard(user: dict = Depends(require_any_role(INVESTOR_ROLES))) -> dict:
    position = INVESTMENT_POSITIONS.get(user["username"], {"total_invested": 0.0, "orders": []})
    projects = len(DASHBOARD_SNAPSHOT["active_projects"])
    return {
        "total_invested": round(position["total_invested"], 2),
        "expected_yield": 0.17,
        "projects": projects,
        "risk_distribution": {"baixo": 0.42, "medio": 0.46, "alto": 0.12},
        "orders": len(position["orders"]),
    }


@app.get("/api/backoffice/dashboard")
def backoffice_dashboard(user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    return {
        "credit": {
            "requests": len(FINANCING_REQUESTS),
            "approved": sum(1 for i in FINANCING_REQUESTS.values() if i["status"] == "approved"),
        },
        "investments": {
            "pf_captacao": round(sum(i.get("allocated_total", 0) for i in INVESTMENT_PRODUCTS.values()), 2),
            "products_open": sum(1 for i in INVESTMENT_PRODUCTS.values() if i["status"] == "open"),
        },
        "treasury": {
            "entries": round(sum(t["amount"] for t in TREASURY_TRANSACTIONS if t["type"] == "investor_inflow"), 2),
            "outflows": round(sum(t["amount"] for t in TREASURY_TRANSACTIONS if t["type"] == "financing_outflow"), 2),
        },
        "compliance": {
            "kyc_pending": sum(1 for v in INVESTOR_ONBOARDINGS.values() if v.get("status") != "approved"),
            "aml_alerts": 0,
        },
        "viewer_role": user["role"],
    }


@app.get("/api/governance/dashboard")
def governance_dashboard(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    pending_kyc = sum(1 for item in INVESTOR_ONBOARDINGS.values() if item.get("status") != "approved")
    summary = [
        {"label": "Comitês no ciclo", "value": "5", "caption": "Ritos ativos no mês"},
        {"label": "Eventos auditáveis", "value": str(len(AUDIT_LOGS) or 3), "caption": "Janela consolidada"},
        {"label": "KYC pendente", "value": str(pending_kyc), "caption": "Fila compliance"},
        {"label": "Funding monitorado", "value": "R$ 48 mi", "caption": "Liquidez institucional"},
    ]
    layers = [
        {
            "tag": "Camada 1",
            "title": "Fachada pública e onboarding",
            "description": "Canais institucionais, entrada de investidores e captação de demanda.",
            "roles": ["marketing", "relacionamento", "investor_pf", "cliente_financiamento"],
        },
        {
            "tag": "Camada 2",
            "title": "Operação de cliente e investidor",
            "description": "Carteira, projetos, dashboard financeiro e experiência autenticada.",
            "roles": ["investor_pf", "investor_pj", "cliente_financiamento"],
        },
        {
            "tag": "Camada 3",
            "title": "Colaborador operacional",
            "description": "Crédito, atendimento, documentos e execução operacional diária.",
            "roles": sorted(COLLABORATOR_ROLES),
        },
        {
            "tag": "Camada 4",
            "title": "Backoffice institucional",
            "description": "Funding, risco, compliance executivo, auditoria e controles.",
            "roles": sorted(BACKOFFICE_ROLES),
        },
        {
            "tag": "Camada 5",
            "title": "Governança e auditoria",
            "description": "Comitês, segregação, aprovação dupla e reporte executivo.",
            "roles": ["diretoria", "governance", "risk_manager"],
        },
    ]
    sla = [
        {"process": "Pré-análise de crédito", "target": "4h úteis"},
        {"process": "Validação compliance/KYC", "target": "D+0"},
        {"process": "Pauta de comitê", "target": "D+1"},
        {"process": "Liberação de funding", "target": "Até 2h após aprovação"},
    ]
    metrics = [
        {"label": "Cobertura de trilha", "value": "100%"},
        {"label": "Segregação crítica", "value": "Ativa"},
        {"label": "Comitês realizados", "value": "12"},
        {"label": "ESG governance", "value": "Em conformidade"},
    ]
    controls = [
        "MFA obrigatório para perfis internos e funções críticas.",
        "Aprovação dupla para operações de maior materialidade.",
        "Auditoria de eventos operacionais e execução de jobs.",
        "Matriz RBAC segregada por camada institucional.",
    ]
    return {
        "summary": summary,
        "layers": layers,
        "sla": sla,
        "metrics": metrics,
        "audit_trail": build_governance_audit_trail(),
        "controls": controls,
    }


@app.get("/api/committees")
def list_committees(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    return {"items": COMMITTEES}


@app.get("/api/committees/decisions")
def list_committee_decisions(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    return {"items": COMMITTEE_DECISIONS[-300:]}


@app.post("/api/committees/decisions", status_code=status.HTTP_201_CREATED)
def create_committee_decision(
    payload: CommitteeDecisionInput,
    user: dict = Depends(require_any_role(BACKOFFICE_ROLES)),
) -> dict:
    item = {
        "id": f"CD-{secrets.token_hex(4).upper()}",
        **payload.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "recorded_by": user["username"],
    }
    COMMITTEE_DECISIONS.append(item)
    audit_log("committees.decision_recorded", user, item)
    return item


@app.get("/api/risk/consolidated")
def risk_consolidated(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    return build_risk_engine()


@app.get("/api/operations/daily-report")
def operation_daily_report(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    return build_daily_operation_report()


@app.get("/api/credit/committee")
def credit_committee(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    queue = build_committee_queue()
    high_materiality = sum(1 for item in queue if item["double_approval"])
    return {
        "summary": [
            {"label": "Casos em pauta", "value": str(len(queue)), "caption": "Fila deliberativa"},
            {"label": "Aprovação dupla", "value": str(high_materiality), "caption": "Materialidade crítica"},
            {"label": "Parecer pendente", "value": "2", "caption": "Risco e compliance"},
        ],
        "members": CREDIT_COMMITTEE_MEMBERS,
        "rules": CREDIT_COMMITTEE_RULES,
        "queue": queue,
        "schedule": [
            {"time": "09:00", "activity": "Fechamento de dossiês e parecer técnico"},
            {"time": "11:30", "activity": "Leitura de garantias e covenant"},
            {"time": "15:00", "activity": "Sessão deliberativa do comitê"},
            {"time": "17:00", "activity": "Ata, decisão e encaminhamento à tesouraria"},
        ],
        "flow": [
            "Originação e triagem",
            "Análise técnica e risco",
            "Compliance e documentação",
            "Comitê deliberativo",
            "Funding e monitoramento",
        ],
    }


@app.get("/api/security/rbac-matrix")
def rbac_matrix(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    return {
        "matrix": [
            {"role": "admin", "investments": "approve", "credit": "approve", "treasury": "supervise", "compliance": "read", "esg": "read"},
            {"role": "risk_manager", "investments": "read", "credit": "approve", "treasury": "read", "compliance": "review", "esg": "review"},
            {"role": "governance", "investments": "read", "credit": "review", "treasury": "read", "compliance": "approve", "esg": "approve"},
            {"role": "diretoria", "investments": "approve", "credit": "approve", "treasury": "approve", "compliance": "read", "esg": "approve"},
            {"role": "tesouraria", "investments": "none", "credit": "none", "treasury": "execute", "compliance": "read", "esg": "none"},
            {"role": "compliance", "investments": "read", "credit": "veto", "treasury": "none", "compliance": "execute", "esg": "read"},
        ],
        "technical_rules": RBAC_TECHNICAL_RULES,
        "layers": [
            {"name": "Camada pública", "scope": "sem acesso a módulos internos"},
            {"name": "Camada cliente/investidor", "scope": "acesso apenas a dados próprios e jornadas autenticadas"},
            {"name": "Camada colaborador", "scope": "execução operacional controlada por função"},
            {"name": "Camada backoffice", "scope": "leitura global e aprovação por escopo institucional"},
        ],
    }


@app.get("/api/jobs/schedules")
def job_schedules(_: dict = Depends(require_any_role(BACKOFFICE_ROLES))) -> dict:
    return {
        "jobs": JOB_SCHEDULES,
        "routines": OPERATIONS_ROUTINES,
        "calendar": ESG_CALENDAR,
    }


@app.get("/liceu/project/{project_id}")
def liceu_project(project_id: str, _: dict = Depends(get_current_user)) -> dict:
    data = LICEU_PROJECTS.get(project_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto nao encontrado")
    return data


@app.get("/liceu/progress/{project_id}")
def liceu_progress(project_id: str, _: dict = Depends(get_current_user)) -> dict:
    data = LICEU_PROJECTS.get(project_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto nao encontrado")
    return {"project_id": project_id, "progress": data["progress"], "stage": data["stage"], "risk": data["risk"]}


@app.get("/api/rules/allocation/{product_id}")
def allocation_rules(product_id: str, _: dict = Depends(get_current_user)) -> dict:
    product = INVESTMENT_PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado")
    return {"product_id": product_id, **resolve_investor_limits(product)}


@app.post("/api/treasury/transactions", status_code=status.HTTP_201_CREATED)
def create_treasury_transaction(
    payload: TreasuryTransactionInput,
    user: dict = Depends(require_any_role({"tesouraria", "admin"})),
) -> dict:
    item = {
        "id": f"TRX-{secrets.token_hex(5).upper()}",
        **payload.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    TREASURY_TRANSACTIONS.append(item)
    audit_log("treasury.transaction_created", user, item)
    return item


@app.get("/api/treasury/transactions")
def list_treasury_transactions(_: dict = Depends(require_any_role({"tesouraria", "admin"}))) -> dict:
    return {"items": TREASURY_TRANSACTIONS}


@app.get("/api/treasury/balance")
def treasury_balance(_: dict = Depends(require_any_role({"tesouraria", "admin"}))) -> dict:
    entries = sum(t["amount"] for t in TREASURY_TRANSACTIONS if t["type"] == "investor_inflow")
    outflows = sum(t["amount"] for t in TREASURY_TRANSACTIONS if t["type"] == "financing_outflow")
    return {"entries": round(entries, 2), "outflows": round(outflows, 2), "balance": round(entries - outflows, 2)}


@app.get("/api/audit/logs")
def list_audit_logs(_: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    return {"items": AUDIT_LOGS[-300:]}


@app.post("/api/jobs/run/{job_name}")
def run_job(job_name: str, user: dict = Depends(require_any_role({"admin", "tesouraria", "compliance", "governance", "risk_manager"}))) -> dict:
    if job_name not in JOB_REGISTRY:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job nao encontrado")

    if job_name == "market_update":
        BASE_INDICATORS["cdi"] = round(BASE_INDICATORS["cdi"] + random.uniform(-0.02, 0.02), 2)
        BASE_INDICATORS["selic"] = round(BASE_INDICATORS["selic"] + random.uniform(-0.01, 0.01), 2)
        event_bus.publish("market.updated", {"source": "manual_job", "indicator": "cdi_selic"})
    elif job_name == "portfolio_risk_score":
        build_risk_engine()
    elif job_name == "liquidity_alerts":
        audit_log("liquidity.alerts_generated", user, {"job_name": job_name, "alerts": 2})
    elif job_name == "liceu_projects_update":
        for project in LICEU_PROJECTS.values():
            project["progress"] = min(100, project["progress"] + random.randint(0, 2))
    elif job_name == "daily_operation_report":
        audit_log("operations.daily_report_generated", user, build_daily_operation_report())
        event_bus.publish("daily.close", {"source": "manual_job", "job_name": job_name})
    elif job_name == "daily_yield_calculation":
        for position in INVESTMENT_POSITIONS.values():
            position["total_invested"] = round(position["total_invested"] * 1.00045, 2)
    elif job_name == "check_product_limits":
        for product in INVESTMENT_PRODUCTS.values():
            if product["allocated_total"] >= product["total_cap_limit"]:
                product["status"] = "closed"
    elif job_name == "sync_liceu_projects":
        for project in LICEU_PROJECTS.values():
            project["progress"] = min(100, project["progress"] + random.randint(0, 2))
    elif job_name == "refresh_governance_snapshot":
        audit_log("governance.snapshot_refreshed", user, {"job_name": job_name, "scope": "executive"})
    elif job_name == "publish_esg_committee_pack":
        audit_log("governance.esg_pack_published", user, {"job_name": job_name, "scope": "esg_committee"})

    audit_log("jobs.executed", user, {"job_name": job_name})
    return {
        "job": job_name,
        "description": JOB_REGISTRY[job_name],
        "status": "completed",
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/careers/apply", status_code=status.HTTP_201_CREATED)
def careers_apply(payload: CareerApplicationInput) -> dict:
    application_id = secrets.token_hex(6).upper()
    return {
        "id": application_id,
        "status": "RECEIVED",
        "message": "Candidatura recebida. Em caso de alinhamento de perfil, entraremos em contato.",
        "data": {
            "name": payload.name,
            "email": payload.email,
            "area": payload.area,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/ml/decision")
def ml_decision(payload: MLDecisionInput) -> dict:
    return run_decision_tree(payload)


SUPPORT_TICKETS: dict = {}


@app.post("/api/support/tickets", status_code=status.HTTP_201_CREATED)
def create_support_ticket(payload: SupportTicketInput) -> dict:
    prefix = datetime.now(timezone.utc).strftime("%Y%m%d")
    ticket_id = f"TKT-{prefix}-{secrets.token_hex(3).upper()}"
    SUPPORT_TICKETS[ticket_id] = {
        "id": ticket_id,
        "subject": payload.subject,
        "message": payload.message,
        "email": payload.email,
        "status": "ABERTO",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return {
        "protocol": ticket_id,
        "status": "ABERTO",
        "message": "Ticket registrado. Nosso time retornara em ate 1 dia util.",
        "created_at": SUPPORT_TICKETS[ticket_id]["created_at"],
    }


@app.get("/api/support/tickets/{ticket_id}")
def get_support_ticket(ticket_id: str) -> dict:
    ticket = SUPPORT_TICKETS.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket nao encontrado.")
    return ticket


# ─────────────────────────────────────────────────────────────────────────────
# PIX — MODELOS
# ─────────────────────────────────────────────────────────────────────────────

class PixChargeInput(BaseModel):
    amount: float = Field(gt=0, le=500_000)
    user_id: str = Field(default="demo", max_length=80)
    description: str = Field(default="Depósito CEA Investimentos", max_length=200)


class PixWebhookPayload(BaseModel):
    txid: str
    status: str          # "paid" | "expired" | "pending"
    amount: float = 0.0
    paid_at: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# PIX — STORES IN-MEMORY
# ─────────────────────────────────────────────────────────────────────────────

PIX_TRANSACTIONS: dict = {}
WALLETS: dict = {}           # user_id -> balance
WALLET_SUBSCRIBERS: dict = {}  # user_id -> list[WebSocket]
PIX_AUDIT_LOGS: list[dict] = []
PIX_PROCESSED_TXIDS: set[str] = set()
LEDGER: list[dict] = []
PIX_RECONCILE_STATE: dict = {"running": False, "last_run": None}
FINANCE_DB_READY: dict = {"ledger": False, "pix_audit": False}

PIX_EXPIRY_MINUTES = 30
PIX_PF_DAILY_LIMIT = 200_000.0
PIX_PF_TX_LIMIT = 50_000.0


def _new_ledger_entry(user_id: str, kind: str, amount: float, reference: str) -> dict:
    item = {
        "id": "LGR" + secrets.token_hex(8).upper(),
        "user_id": user_id,
        "type": kind,
        "amount": round(amount, 2),
        "reference": reference,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    LEDGER.append(item)
    _persist_ledger_entry_db(item)
    return item


def _ensure_finance_tables() -> None:
    if FINANCE_DB_READY["ledger"] and FINANCE_DB_READY["pix_audit"]:
        return

    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS ledger_entries (
                    id VARCHAR(40) PRIMARY KEY,
                    user_id VARCHAR(120) NOT NULL,
                    type VARCHAR(60) NOT NULL,
                    amount NUMERIC(18,2) NOT NULL,
                    reference VARCHAR(120) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS pix_audit_entries (
                    id VARCHAR(40) PRIMARY KEY,
                    action VARCHAR(80) NOT NULL,
                    username VARCHAR(120) NOT NULL,
                    txid VARCHAR(80) NOT NULL,
                    ip VARCHAR(64),
                    device TEXT,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                    details TEXT
                )
                """
            )
        )
        db.commit()
        FINANCE_DB_READY["ledger"] = True
        FINANCE_DB_READY["pix_audit"] = True
    except Exception:
        db.rollback()
    finally:
        db.close()


def _persist_ledger_entry_db(item: dict) -> None:
    _ensure_finance_tables()
    if not FINANCE_DB_READY["ledger"]:
        return

    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                INSERT INTO ledger_entries (id, user_id, type, amount, reference, created_at)
                VALUES (:id, :user_id, :type, :amount, :reference, :created_at)
                """
            ),
            item,
        )
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def _persist_pix_audit_db(item: dict) -> None:
    _ensure_finance_tables()
    if not FINANCE_DB_READY["pix_audit"]:
        return

    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                INSERT INTO pix_audit_entries (id, action, username, txid, ip, device, timestamp, details)
                VALUES (:id, :action, :username, :txid, :ip, :device, :timestamp, :details)
                """
            ),
            {
                "id": item["id"],
                "action": item["action"],
                "username": item["user"],
                "txid": item["txid"],
                "ip": item.get("ip"),
                "device": item.get("device"),
                "timestamp": item["timestamp"],
                "details": json.dumps({k: v for k, v in item.items() if k not in {"id", "action", "user", "txid", "ip", "device", "timestamp"}}),
            },
        )
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def _user_profile_type(user_id: str) -> str:
    user = DEMO_USERS.get(user_id)
    if not user:
        return "PJ"
    return "PF" if user.get("role") == "investor_pf" else "PJ"


def _same_utc_day(iso_ts: str | None) -> bool:
    if not iso_ts:
        return False
    try:
        dt = datetime.fromisoformat(iso_ts)
    except Exception:
        return False
    now = datetime.now(timezone.utc)
    return dt.date() == now.date()


def _daily_paid_pix_total(user_id: str) -> float:
    total = 0.0
    for tx in PIX_TRANSACTIONS.values():
        if tx.get("user_id") == user_id and tx.get("status") == "paid" and _same_utc_day(tx.get("paid_at")):
            total += float(tx.get("amount", 0))
    return round(total, 2)


def validate_pix_limit(user_id: str, amount: float) -> None:
    profile_type = _user_profile_type(user_id)
    if profile_type != "PF":
        return
    if amount > PIX_PF_TX_LIMIT:
        raise HTTPException(status_code=422, detail="Limite PF por transacao excedido (50.000).")
    daily_total = _daily_paid_pix_total(user_id)
    if daily_total + amount > PIX_PF_DAILY_LIMIT:
        raise HTTPException(status_code=422, detail="Limite PF diario excedido (200.000).")


def _pix_audit(action: str, request: Request | None, user_id: str, txid: str, extra: dict | None = None) -> None:
    item = {
        "id": "PXA" + secrets.token_hex(6).upper(),
        "action": action,
        "user": user_id,
        "txid": txid,
        "ip": request.client.host if request and request.client else "unknown",
        "device": request.headers.get("user-agent", "unknown") if request else "unknown",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **(extra or {}),
    }
    PIX_AUDIT_LOGS.append(item)
    _persist_pix_audit_db(item)


def _get_wallet(user_id: str) -> dict:
    if user_id not in WALLETS:
        WALLETS[user_id] = {
            "user_id": user_id,
            "balance": 0.0,
            "locked": 0.0,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    else:
        WALLETS[user_id].setdefault("locked", 0.0)
    return WALLETS[user_id]


async def _broadcast_wallet(user_id: str) -> None:
    subs = WALLET_SUBSCRIBERS.get(user_id, [])
    wallet = _get_wallet(user_id)
    dead = []
    for ws in subs:
        try:
            await ws.send_json(
                {
                    "event": "wallet.updated",
                    "balance": wallet["balance"],
                    "locked": wallet.get("locked", 0.0),
                    "total": round(wallet["balance"] + wallet.get("locked", 0.0), 2),
                    "updated_at": wallet["updated_at"],
                }
            )
        except Exception:
            dead.append(ws)
    for ws in dead:
        subs.remove(ws)


# ─────────────────────────────────────────────────────────────────────────────
# PIX — ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/pix/create", status_code=status.HTTP_201_CREATED)
def create_pix_charge(payload: PixChargeInput) -> dict:
    validate_pix_limit(payload.user_id, payload.amount)
    txid = f"CEA{secrets.token_hex(10).upper()}"
    created_at = datetime.now(timezone.utc)
    expires_at = created_at.timestamp() + PIX_EXPIRY_MINUTES * 60

    # Payload QRCODE simulado — em produção viria do PSP/banco parceiro
    qrcode_payload = (
        f"00020126580014BR.GOV.BCB.PIX0136{txid}"
        f"5204000053039865802BR5913CEA Invest6008Sao Paulo"
        f"62070503***6304ABCD"
    )

    PIX_TRANSACTIONS[txid] = {
        "txid": txid,
        "user_id": payload.user_id,
        "amount": payload.amount,
        "description": payload.description,
        "status": "pending",
        "qrcode": qrcode_payload,
        "created_at": created_at.isoformat(),
        "expires_at": datetime.fromtimestamp(expires_at, tz=timezone.utc).isoformat(),
        "paid_at": None,
        "credited": False,
    }

    return {
        "txid": txid,
        "amount": payload.amount,
        "qrcode": qrcode_payload,
        "expires_at": PIX_TRANSACTIONS[txid]["expires_at"],
        "status": "pending",
    }


@app.get("/api/pix/status/{txid}")
def get_pix_status(txid: str) -> dict:
    tx = PIX_TRANSACTIONS.get(txid)
    if not tx:
        raise HTTPException(status_code=404, detail="Transacao PIX nao encontrada.")
    return tx


def _gateway_check(tx: dict) -> str:
    if tx.get("status") == "paid":
        return "paid"
    try:
        exp = datetime.fromisoformat(tx["expires_at"])
    except Exception:
        return tx.get("status", "pending")
    if exp < datetime.now(timezone.utc):
        return "expired"
    return tx.get("status", "pending")


async def _credit_wallet_for_pix(tx: dict, amount: float, request: Request | None = None) -> dict:
    txid = tx["txid"]
    if txid in PIX_PROCESSED_TXIDS or tx.get("credited"):
        return {"ok": True, "detail": "already_processed"}

    validate_pix_limit(tx["user_id"], amount)
    wallet = _get_wallet(tx["user_id"])
    wallet["balance"] = round(wallet["balance"] + amount, 2)
    wallet["updated_at"] = datetime.now(timezone.utc).isoformat()
    tx["credited"] = True
    PIX_PROCESSED_TXIDS.add(txid)
    _new_ledger_entry(tx["user_id"], "deposito_pix", amount, txid)
    _pix_audit("pix.credit", request, tx["user_id"], txid, {"amount": amount})
    await _broadcast_wallet(tx["user_id"])
    return {"ok": True, "detail": "credited"}


@app.post("/api/pix/webhook")
async def pix_webhook(payload: PixWebhookPayload, request: Request) -> dict:
    """
    Endpoint chamado pelo PSP/banco ao confirmar o pagamento.
    Valida txid, credita carteira e notifica via WebSocket.
    """
    tx = PIX_TRANSACTIONS.get(payload.txid)
    if not tx:
        raise HTTPException(status_code=404, detail="txid nao encontrado.")

    if payload.txid in PIX_PROCESSED_TXIDS or tx.get("credited"):
        return {"ok": True, "detail": "already_paid"}

    tx["status"] = payload.status
    if payload.status == "paid":
        tx["paid_at"] = payload.paid_at or datetime.now(timezone.utc).isoformat()
        amount = payload.amount if payload.amount > 0 else tx["amount"]
        await _credit_wallet_for_pix(tx, amount, request)

    _pix_audit("pix.webhook", request, tx["user_id"], payload.txid, {"status": payload.status})

    return {"ok": True, "txid": payload.txid, "status": payload.status}


@app.post("/api/pix/reconcile")
async def reconcile_pix(user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    require_pix_action("pix.reconcile", user)
    pending = [tx for tx in PIX_TRANSACTIONS.values() if tx.get("status") == "pending"]
    reconciled = 0
    expired = 0
    already = 0

    for tx in pending:
        status = _gateway_check(tx)
        txid = tx["txid"]
        if status == "paid":
            if txid in PIX_PROCESSED_TXIDS or tx.get("credited"):
                already += 1
                continue
            tx["paid_at"] = tx.get("paid_at") or datetime.now(timezone.utc).isoformat()
            tx["status"] = "paid"
            await _credit_wallet_for_pix(tx, float(tx.get("amount", 0)))
            reconciled += 1
        elif status == "expired":
            tx["status"] = "expired"
            expired += 1

    PIX_RECONCILE_STATE["running"] = True
    PIX_RECONCILE_STATE["last_run"] = datetime.now(timezone.utc).isoformat()
    audit_log("pix.reconcile", user, {"reconciled": reconciled, "expired": expired, "already": already})
    return {
        "ok": True,
        "checked": len(pending),
        "reconciled": reconciled,
        "already_processed": already,
        "expired": expired,
        "last_run": PIX_RECONCILE_STATE["last_run"],
    }


async def _pix_reconcile_loop() -> None:
    while True:
        try:
            pending = [tx for tx in PIX_TRANSACTIONS.values() if tx.get("status") == "pending"]
            for tx in pending:
                status = _gateway_check(tx)
                if status == "paid" and tx["txid"] not in PIX_PROCESSED_TXIDS and not tx.get("credited"):
                    tx["paid_at"] = tx.get("paid_at") or datetime.now(timezone.utc).isoformat()
                    tx["status"] = "paid"
                    await _credit_wallet_for_pix(tx, float(tx.get("amount", 0)))
                elif status == "expired":
                    tx["status"] = "expired"
            PIX_RECONCILE_STATE["last_run"] = datetime.now(timezone.utc).isoformat()
            PIX_RECONCILE_STATE["running"] = True
        except Exception:
            PIX_RECONCILE_STATE["running"] = False
        await asyncio.sleep(300)

@app.get("/api/pix/reconcile/status")
def reconcile_status(user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    require_pix_action("pix.reconcile", user)
    return {
        "running": PIX_RECONCILE_STATE.get("running", False),
        "last_run": PIX_RECONCILE_STATE.get("last_run"),
        "interval_seconds": 300,
    }


# ─────────────────────────────────────────────────────────────────────────────
# WALLET — ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/wallet/balance")
def wallet_balance(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    wallet = _get_wallet(uid)
    return {
        **wallet,
        "total": round(wallet["balance"] + wallet.get("locked", 0.0), 2),
    }


@app.websocket("/ws/wallet/{user_id}")
async def wallet_stream(websocket: WebSocket, user_id: str) -> None:
    await websocket.accept()
    if user_id not in WALLET_SUBSCRIBERS:
        WALLET_SUBSCRIBERS[user_id] = []
    WALLET_SUBSCRIBERS[user_id].append(websocket)
    try:
        # enviar saldo atual imediatamente
        await websocket.send_json({
            "event": "wallet_balance",
            **_get_wallet(user_id),
            "total": round(_get_wallet(user_id)["balance"] + _get_wallet(user_id).get("locked", 0.0), 2),
        })
        while True:
            # manter conexão viva aguardando mensagens do cliente
            await websocket.receive_text()
    except WebSocketDisconnect:
        subs = WALLET_SUBSCRIBERS.get(user_id, [])
        if websocket in subs:
            subs.remove(websocket)


# =============================================================================
# SAQUE PIX
# =============================================================================

class PixWithdrawInput(BaseModel):
    amount: float
    user_id: str
    pix_key: str
    key_type: str = "cpf"   # cpf | cnpj | email | phone | random
    mfa_code: str


PIX_WITHDRAWALS: dict = {}   # wid -> record


@app.post("/api/pix/withdraw", status_code=status.HTTP_201_CREATED)
async def pix_withdraw(payload: PixWithdrawInput, user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", payload.user_id)
    wallet = _get_wallet(uid)

    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero.")
    if wallet["balance"] < payload.amount:
        raise HTTPException(status_code=422, detail="Saldo insuficiente.")
    expected_mfa = DEMO_USERS.get(uid, {}).get("mfa_code")
    if expected_mfa and payload.mfa_code != expected_mfa:
        raise HTTPException(status_code=401, detail="MFA invalido para saque PIX.")

    wid = "WIT" + secrets.token_hex(10).upper()
    PIX_WITHDRAWALS[wid] = {
        "wid": wid,
        "user_id": uid,
        "amount": payload.amount,
        "pix_key": payload.pix_key,
        "key_type": payload.key_type,
        "status": "pending_approval",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "settled_at": None,
        "approved_by": [],
        "approval_count": 0,
        "required_approvals": 2,
    }
    return {"wid": wid, "status": "pending_approval", "amount": payload.amount}


@app.post("/api/pix/withdraw/approve/{wid}")
async def approve_pix_withdraw(wid: str, approver: dict = Depends(require_any_role({"admin", "tesouraria", "risk_manager"}))) -> dict:
    require_pix_action("pix.withdraw.approve", approver)
    w = PIX_WITHDRAWALS.get(wid)
    if not w:
        raise HTTPException(status_code=404, detail="Solicitacao de saque nao encontrada.")
    if w["status"] == "settled":
        return {"ok": True, "detail": "already_settled", "wid": wid}
    if w["status"] not in {"pending_approval", "approved_stage_1"}:
        raise HTTPException(status_code=422, detail="Solicitacao nao esta pendente para aprovacao.")

    already = [a for a in w.get("approved_by", []) if a.get("username") == approver.get("username")]
    if already:
        raise HTTPException(status_code=422, detail="Este aprovador ja aprovou esta solicitacao.")

    w.setdefault("approved_by", [])
    w["approved_by"].append(
        {
            "username": approver.get("username"),
            "role": approver.get("role"),
            "approved_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    w["approval_count"] = len(w["approved_by"])

    if w["approval_count"] < w.get("required_approvals", 2):
        w["status"] = "approved_stage_1"
        return {
            "ok": True,
            "wid": wid,
            "status": w["status"],
            "approval_count": w["approval_count"],
            "required_approvals": w.get("required_approvals", 2),
        }

    roles = {a.get("role") for a in w["approved_by"]}
    dual_role_ok = ("tesouraria" in roles and "risk_manager" in roles) or ("admin" in roles and len(roles) >= 2)
    if not dual_role_ok:
        raise HTTPException(status_code=422, detail="Aprovacao dupla exige segregacao de perfis (tesouraria + risk_manager, ou admin + outro).")

    wallet = _get_wallet(w["user_id"])
    if wallet["balance"] < w["amount"]:
        raise HTTPException(status_code=422, detail="Saldo insuficiente no momento da aprovacao.")

    wallet["balance"] = round(wallet["balance"] - w["amount"], 2)
    wallet["updated_at"] = datetime.now(timezone.utc).isoformat()
    w["status"] = "settled"
    w["settled_at"] = datetime.now(timezone.utc).isoformat()
    _new_ledger_entry(w["user_id"], "resgate", w["amount"], wid)
    await _broadcast_wallet(w["user_id"])
    return {"ok": True, "wid": wid, "status": "settled", "new_balance": wallet["balance"]}


@app.get("/api/pix/withdrawals")
def list_withdrawals(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    items = [v for v in PIX_WITHDRAWALS.values() if v["user_id"] == uid]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@app.get("/api/pix/withdrawals/pending")
def list_pending_withdrawals(user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    require_pix_action("pix.withdraw.approve", user)
    items = [
        v for v in PIX_WITHDRAWALS.values()
        if v.get("status") in {"pending_approval", "approved_stage_1"}
    ]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@app.post("/api/pix/withdraw/reject/{wid}")
def reject_pix_withdraw(wid: str, approver: dict = Depends(require_any_role({"admin", "tesouraria", "risk_manager"}))) -> dict:
    require_pix_action("pix.withdraw.approve", approver)
    w = PIX_WITHDRAWALS.get(wid)
    if not w:
        raise HTTPException(status_code=404, detail="Solicitacao de saque nao encontrada.")
    if w.get("status") == "settled":
        raise HTTPException(status_code=422, detail="Solicitacao ja liquidada, nao pode ser rejeitada.")

    w["status"] = "rejected"
    w["rejected_by"] = approver.get("username")
    w["rejected_at"] = datetime.now(timezone.utc).isoformat()
    return {"ok": True, "wid": wid, "status": "rejected"}


# =============================================================================
# CONTA DIGITAL CEA — extrato unificado
# =============================================================================

@app.get("/api/account/details")
def account_details(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    wallet = _get_wallet(uid)
    # número de conta simulado (determinístico por user_id)
    acc_num = str(abs(hash(uid)) % 10_000_000).zfill(7) + "-" + str(abs(hash(uid + "_d")) % 10)
    return {
        "user_id": uid,
        "account_number": acc_num,
        "agency": "0001",
        "bank_name": "CEA Investimentos",
        "ispb": "00000000",
        "balance": wallet["balance"],
        "locked": wallet.get("locked", 0.0),
        "total": round(wallet["balance"] + wallet.get("locked", 0.0), 2),
        "updated_at": wallet["updated_at"],
    }


@app.get("/api/account/statement")
def account_statement(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")

    entries: list = []

    # depósitos PIX
    for tx in PIX_TRANSACTIONS.values():
        if tx.get("user_id") == uid and tx.get("status") == "paid":
            entries.append({
                "id": tx["txid"], "type": "deposit", "label": "Depósito PIX",
                "amount": tx["amount"], "sign": "+",
                "at": tx.get("paid_at", tx.get("created_at", "")),
            })

    # saques
    for w in PIX_WITHDRAWALS.values():
        if w["user_id"] == uid:
            entries.append({
                "id": w["wid"], "type": "withdraw", "label": "Saque PIX",
                "amount": w["amount"], "sign": "-",
                "at": w["created_at"],
            })

    # rendimentos
    for yp in YIELD_PAYMENTS.values():
        for inv in yp.get("investors", []):
            if inv["user_id"] == uid:
                entries.append({
                    "id": yp["payment_id"] + "_" + uid, "type": "yield",
                    "label": f"Rendimento — {yp.get('project_id', '')}",
                    "amount": inv["amount"], "sign": "+",
                    "at": yp["paid_at"],
                })

    # splits de projetos
    for sp in PROJECT_SPLITS.values():
        for rec in sp.get("recipients", []):
            if rec["user_id"] == uid:
                entries.append({
                    "id": sp["split_id"] + "_" + uid, "type": "split",
                    "label": f"Split — {sp.get('project_id', '')}",
                    "amount": rec["credited"], "sign": "+",
                    "at": sp["executed_at"],
                })

    entries.sort(key=lambda x: x["at"], reverse=True)
    wallet = _get_wallet(uid)
    return {
        "balance": wallet["balance"],
        "locked": wallet.get("locked", 0.0),
        "total": round(wallet["balance"] + wallet.get("locked", 0.0), 2),
        "entries": entries,
    }


# =============================================================================
# SPLIT DE PAGAMENTOS — PROJETOS
# =============================================================================

class SplitRecipient(BaseModel):
    user_id: str
    percentage: float   # 0–100


class ProjectSplitInput(BaseModel):
    project_id: str
    total_amount: float
    recipients: list[SplitRecipient]
    description: str = ""


PROJECT_SPLITS: dict = {}   # split_id -> record


@app.post("/api/projects/split", status_code=status.HTTP_201_CREATED)
async def execute_split(payload: ProjectSplitInput, user: dict = Depends(get_current_user)) -> dict:
    if not payload.recipients:
        raise HTTPException(status_code=400, detail="Lista de destinatários vazia.")

    total_pct = sum(r.percentage for r in payload.recipients)
    if round(total_pct, 4) != 100.0:
        raise HTTPException(status_code=422, detail=f"Percentuais somam {total_pct:.2f}%, devem somar 100%.")

    if payload.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero.")

    split_id = "SPL" + secrets.token_hex(9).upper()
    distributed: list = []

    for r in payload.recipients:
        credited = round(payload.total_amount * r.percentage / 100, 2)
        wallet = _get_wallet(r.user_id)
        wallet["balance"] = round(wallet["balance"] + credited, 2)
        wallet["updated_at"] = datetime.now(timezone.utc).isoformat()
        await _broadcast_wallet(r.user_id)
        distributed.append({"user_id": r.user_id, "percentage": r.percentage, "credited": credited})

    PROJECT_SPLITS[split_id] = {
        "split_id": split_id,
        "project_id": payload.project_id,
        "total_amount": payload.total_amount,
        "description": payload.description,
        "recipients": distributed,
        "executed_by": user.get("sub", "system"),
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }

    return {"split_id": split_id, "distributed": distributed}


@app.get("/api/projects/splits")
def list_splits(user: dict = Depends(get_current_user)) -> dict:
    items = list(PROJECT_SPLITS.values())
    items.sort(key=lambda x: x["executed_at"], reverse=True)
    return {"items": items}


# =============================================================================
# RENDIMENTOS AUTOMÁTICOS
# =============================================================================

class YieldScheduleInput(BaseModel):
    project_id: str
    rate: float                  # % ao mês, ex: 1.2
    frequency: str = "monthly"   # monthly | weekly | daily
    investors: list[dict]        # [{user_id, principal}]


class YieldPayInput(BaseModel):
    schedule_id: str


YIELD_SCHEDULES: dict = {}   # schedule_id -> schedule
YIELD_PAYMENTS: dict = {}    # payment_id -> record


@app.post("/api/yields/schedule", status_code=status.HTTP_201_CREATED)
def create_yield_schedule(payload: YieldScheduleInput, user: dict = Depends(get_current_user)) -> dict:
    sid = "YS" + secrets.token_hex(9).upper()
    YIELD_SCHEDULES[sid] = {
        "schedule_id": sid,
        "project_id": payload.project_id,
        "rate": payload.rate,
        "frequency": payload.frequency,
        "investors": payload.investors,
        "active": True,
        "created_by": user.get("sub", "system"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_paid_at": None,
    }
    return YIELD_SCHEDULES[sid]


@app.get("/api/yields/schedules")
def list_yield_schedules(user: dict = Depends(get_current_user)) -> dict:
    return {"items": list(YIELD_SCHEDULES.values())}


@app.post("/api/yields/pay")
async def pay_yield(payload: YieldPayInput, user: dict = Depends(get_current_user)) -> dict:
    """Dispara pagamento de rendimento para um schedule."""
    sched = YIELD_SCHEDULES.get(payload.schedule_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule não encontrado.")

    paid_at = datetime.now(timezone.utc).isoformat()
    payment_id = "YP" + secrets.token_hex(9).upper()
    paid_investors: list = []

    for inv in sched.get("investors", []):
        uid = inv["user_id"]
        principal = float(inv.get("principal", 0))
        amount = round(principal * sched["rate"] / 100, 2)

        wallet = _get_wallet(uid)
        wallet["balance"] = round(wallet["balance"] + amount, 2)
        wallet["updated_at"] = paid_at
        _new_ledger_entry(uid, "rendimento", amount, payment_id)
        await _broadcast_wallet(uid)

        paid_investors.append({"user_id": uid, "principal": principal, "rate": sched["rate"], "amount": amount})

    YIELD_PAYMENTS[payment_id] = {
        "payment_id": payment_id,
        "schedule_id": payload.schedule_id,
        "project_id": sched["project_id"],
        "paid_at": paid_at,
        "investors": paid_investors,
        "triggered_by": user.get("sub", "system"),
    }

    sched["last_paid_at"] = paid_at
    return {"payment_id": payment_id, "investors_paid": len(paid_investors), "paid_at": paid_at}


@app.get("/api/yields/payments")
def list_yield_payments(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    # retorna apenas pagamentos onde o user aparece
    result = []
    for p in YIELD_PAYMENTS.values():
        my = [i for i in p.get("investors", []) if i["user_id"] == uid]
        if my:
            result.append({**p, "my_amount": sum(i["amount"] for i in my)})
    result.sort(key=lambda x: x["paid_at"], reverse=True)
    return {"items": result}


@app.get("/api/pix/audit")
def pix_audit_logs(user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    require_pix_action("pix.audit", user)
    items = PIX_AUDIT_LOGS[-500:]
    items.sort(key=lambda x: x["timestamp"], reverse=True)
    return {"items": items}


@app.get("/api/ledger")
def list_ledger(user: dict = Depends(get_current_user)) -> dict:
    uid = user["username"]
    if user["role"] in STAFF_ROLES:
        items = LEDGER[-1000:]
    else:
        items = [i for i in LEDGER if i["user_id"] == uid]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@app.get("/api/pix/kpis")
def pix_kpis(user: dict = Depends(require_any_role(STAFF_ROLES))) -> dict:
    require_pix_action("pix.kpis", user)
    today_paid = [tx for tx in PIX_TRANSACTIONS.values() if tx.get("status") == "paid" and _same_utc_day(tx.get("paid_at"))]
    volume_daily = round(sum(float(tx.get("amount", 0)) for tx in today_paid), 2)
    ticket_medio = round(volume_daily / len(today_paid), 2) if today_paid else 0.0

    invest_orders_today = [o for o in INVESTMENT_ORDERS if _same_utc_day(o.get("created_at"))]
    conversao = round((len(invest_orders_today) / len(today_paid)) * 100, 2) if today_paid else 0.0

    wallets = list(WALLETS.values())
    saldo_medio = round(sum(w.get("balance", 0) for w in wallets) / len(wallets), 2) if wallets else 0.0
    total_disponivel = round(sum(w.get("balance", 0) for w in wallets), 2)
    total_bloqueado = round(sum(w.get("locked", 0) for w in wallets), 2)
    liquidez = round((total_disponivel / (total_disponivel + total_bloqueado)) * 100, 2) if (total_disponivel + total_bloqueado) > 0 else 100.0

    return {
        "pix_volume_diario": volume_daily,
        "ticket_medio": ticket_medio,
        "conversao_investimento_pct": conversao,
        "saldo_medio_carteira": saldo_medio,
        "liquidez_pct": liquidez,
        "wallet_disponivel_total": total_disponivel,
        "wallet_bloqueado_total": total_bloqueado,
    }


@app.get("/api/finance/flow")
def finance_flow(user: dict = Depends(get_current_user)) -> dict:
    return {
        "flow": [
            "PIX",
            "Carteira",
            "Investimento",
            "Projeto LICEU",
            "Retorno",
            "Carteira",
            "Saque PIX",
        ]
    }


# =============================================================================
# ASSINATURA DIGITAL DE CONTRATOS
# =============================================================================

class ContractCreateInput(BaseModel):
    title: str
    counterparties: list[str]
    content_hash: str


class ContractSignInput(BaseModel):
    contract_id: str
    signature_token: str


DIGITAL_CONTRACTS: dict = {}


@app.post("/api/contracts/create", status_code=status.HTTP_201_CREATED)
def create_contract(payload: ContractCreateInput, user: dict = Depends(get_current_user)) -> dict:
    cid = "CTR" + secrets.token_hex(8).upper()
    created_by = user.get("sub", "system")
    counterparties = list(dict.fromkeys(payload.counterparties + [created_by]))
    signatures = [{"signer_id": s, "signed": False, "signed_at": None, "token_tail": None} for s in counterparties]

    DIGITAL_CONTRACTS[cid] = {
        "contract_id": cid,
        "title": payload.title,
        "content_hash": payload.content_hash,
        "counterparties": counterparties,
        "signatures": signatures,
        "status": "pending_signatures",
        "created_by": created_by,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return DIGITAL_CONTRACTS[cid]


@app.post("/api/contracts/sign")
def sign_contract(payload: ContractSignInput, user: dict = Depends(get_current_user)) -> dict:
    contract = DIGITAL_CONTRACTS.get(payload.contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contrato nao encontrado.")

    signer = user.get("sub", "demo")
    row = next((s for s in contract["signatures"] if s["signer_id"] == signer), None)
    if not row:
        raise HTTPException(status_code=403, detail="Usuario nao habilitado para assinar este contrato.")
    if row["signed"]:
        return {"ok": True, "status": contract["status"], "detail": "already_signed"}

    row["signed"] = True
    row["signed_at"] = datetime.now(timezone.utc).isoformat()
    row["token_tail"] = payload.signature_token[-6:] if payload.signature_token else None

    if all(s["signed"] for s in contract["signatures"]):
        contract["status"] = "fully_signed"
        contract["completed_at"] = datetime.now(timezone.utc).isoformat()

    return {"ok": True, "contract_id": payload.contract_id, "status": contract["status"]}


@app.get("/api/contracts")
def list_contracts(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    items = [c for c in DIGITAL_CONTRACTS.values() if uid in c.get("counterparties", [])]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@app.get("/api/contracts/{contract_id}")
def get_contract(contract_id: str, user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    c = DIGITAL_CONTRACTS.get(contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contrato nao encontrado.")
    if uid not in c.get("counterparties", []):
        raise HTTPException(status_code=403, detail="Sem acesso a este contrato.")
    return c


# =============================================================================
# TOKENIZACAO DE INVESTIMENTOS
# =============================================================================

class TokenCreateInput(BaseModel):
    project_id: str
    token_symbol: str
    total_supply: int
    price_brl: float


class TokenBuyInput(BaseModel):
    token_id: str
    quantity: int


TOKEN_ASSETS: dict = {}
TOKEN_HOLDINGS: dict = {}
TOKEN_ORDERS: dict = {}


@app.post("/api/tokens/create", status_code=status.HTTP_201_CREATED)
def create_token_asset(payload: TokenCreateInput, user: dict = Depends(get_current_user)) -> dict:
    if payload.total_supply <= 0 or payload.price_brl <= 0:
        raise HTTPException(status_code=400, detail="Supply e preco devem ser maiores que zero.")

    tid = "TOK" + secrets.token_hex(7).upper()
    TOKEN_ASSETS[tid] = {
        "token_id": tid,
        "project_id": payload.project_id,
        "token_symbol": payload.token_symbol.upper(),
        "total_supply": payload.total_supply,
        "available_supply": payload.total_supply,
        "price_brl": payload.price_brl,
        "issuer": user.get("sub", "system"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return TOKEN_ASSETS[tid]


@app.get("/api/tokens/market")
def list_token_market(user: dict = Depends(get_current_user)) -> dict:
    items = list(TOKEN_ASSETS.values())
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@app.post("/api/tokens/buy")
async def buy_token(payload: TokenBuyInput, user: dict = Depends(get_current_user)) -> dict:
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantidade invalida.")

    token = TOKEN_ASSETS.get(payload.token_id)
    if not token:
        raise HTTPException(status_code=404, detail="Token nao encontrado.")
    if token["available_supply"] < payload.quantity:
        raise HTTPException(status_code=422, detail="Liquidez insuficiente para essa compra.")

    uid = user.get("sub", "demo")
    total_cost = round(payload.quantity * token["price_brl"], 2)
    wallet = _get_wallet(uid)
    if wallet["balance"] < total_cost:
        raise HTTPException(status_code=422, detail="Saldo insuficiente na wallet interna.")

    wallet["balance"] = round(wallet["balance"] - total_cost, 2)
    wallet["updated_at"] = datetime.now(timezone.utc).isoformat()
    await _broadcast_wallet(uid)

    token["available_supply"] -= payload.quantity
    TOKEN_HOLDINGS.setdefault(uid, {})
    TOKEN_HOLDINGS[uid][payload.token_id] = TOKEN_HOLDINGS[uid].get(payload.token_id, 0) + payload.quantity

    oid = "ORD" + secrets.token_hex(8).upper()
    TOKEN_ORDERS[oid] = {
        "order_id": oid,
        "user_id": uid,
        "token_id": payload.token_id,
        "quantity": payload.quantity,
        "unit_price": token["price_brl"],
        "total_cost": total_cost,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    return {"order_id": oid, "wallet_balance": wallet["balance"], "position_qty": TOKEN_HOLDINGS[uid][payload.token_id]}


@app.get("/api/tokens/portfolio")
def token_portfolio(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    holding = TOKEN_HOLDINGS.get(uid, {})
    items = []
    for tid, qty in holding.items():
        asset = TOKEN_ASSETS.get(tid)
        if not asset:
            continue
        items.append({
            "token_id": tid,
            "token_symbol": asset["token_symbol"],
            "project_id": asset["project_id"],
            "quantity": qty,
            "mark_price": asset["price_brl"],
            "mark_value": round(qty * asset["price_brl"], 2),
        })
    return {"items": items}


# =============================================================================
# WALLET INTERNA
# =============================================================================

class WalletTransferInput(BaseModel):
    to_user_id: str
    amount: float
    description: str = ""


WALLET_TRANSFERS: dict = {}


@app.post("/api/wallet/transfer", status_code=status.HTTP_201_CREATED)
async def wallet_transfer(payload: WalletTransferInput, user: dict = Depends(get_current_user)) -> dict:
    from_uid = user.get("sub", "demo")
    to_uid = payload.to_user_id
    if from_uid == to_uid:
        raise HTTPException(status_code=400, detail="Transferencia para a mesma conta nao permitida.")
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero.")

    origin = _get_wallet(from_uid)
    target = _get_wallet(to_uid)
    if origin["balance"] < payload.amount:
        raise HTTPException(status_code=422, detail="Saldo insuficiente.")

    origin["balance"] = round(origin["balance"] - payload.amount, 2)
    target["balance"] = round(target["balance"] + payload.amount, 2)
    now = datetime.now(timezone.utc).isoformat()
    origin["updated_at"] = now
    target["updated_at"] = now

    transfer_id = "TRF" + secrets.token_hex(8).upper()
    WALLET_TRANSFERS[transfer_id] = {
        "transfer_id": transfer_id,
        "from_user_id": from_uid,
        "to_user_id": to_uid,
        "amount": payload.amount,
        "description": payload.description,
        "status": "settled",
        "created_at": now,
    }

    await _broadcast_wallet(from_uid)
    await _broadcast_wallet(to_uid)
    return {"transfer_id": transfer_id, "status": "settled", "from_balance": origin["balance"]}


@app.get("/api/wallet/transfers")
def list_wallet_transfers(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    items = [
        t for t in WALLET_TRANSFERS.values()
        if t["from_user_id"] == uid or t["to_user_id"] == uid
    ]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


# =============================================================================
# MARKETPLACE DE PROJETOS
# =============================================================================

class MarketplaceProjectCreateInput(BaseModel):
    project_id: str
    title: str
    category: str
    target_raise: float
    minimum_ticket: float
    annual_yield_est: float


class MarketplaceInvestInput(BaseModel):
    project_id: str
    amount: float


MARKETPLACE_PROJECTS: dict = {
    "PRJ-ALPHA": {
        "project_id": "PRJ-ALPHA",
        "title": "Residencial Alpha",
        "category": "Imobiliario",
        "target_raise": 3500000.0,
        "raised": 1125000.0,
        "minimum_ticket": 1000.0,
        "annual_yield_est": 12.8,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
    "PRJ-BETA": {
        "project_id": "PRJ-BETA",
        "title": "Infra Hub Beta",
        "category": "Infraestrutura",
        "target_raise": 5200000.0,
        "raised": 2280000.0,
        "minimum_ticket": 2500.0,
        "annual_yield_est": 14.2,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
}
MARKETPLACE_ORDERS: dict = {}


@app.get("/api/marketplace/projects")
def list_marketplace_projects(user: dict = Depends(get_current_user)) -> dict:
    items = list(MARKETPLACE_PROJECTS.values())
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@app.post("/api/marketplace/projects", status_code=status.HTTP_201_CREATED)
def create_marketplace_project(payload: MarketplaceProjectCreateInput, user: dict = Depends(get_current_user)) -> dict:
    if payload.target_raise <= 0 or payload.minimum_ticket <= 0:
        raise HTTPException(status_code=400, detail="Valores invalidos.")
    MARKETPLACE_PROJECTS[payload.project_id] = {
        "project_id": payload.project_id,
        "title": payload.title,
        "category": payload.category,
        "target_raise": payload.target_raise,
        "raised": 0.0,
        "minimum_ticket": payload.minimum_ticket,
        "annual_yield_est": payload.annual_yield_est,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "created_by": user.get("sub", "system"),
    }
    return MARKETPLACE_PROJECTS[payload.project_id]


@app.post("/api/marketplace/invest", status_code=status.HTTP_201_CREATED)
async def invest_marketplace(payload: MarketplaceInvestInput, user: dict = Depends(get_current_user)) -> dict:
    prj = MARKETPLACE_PROJECTS.get(payload.project_id)
    if not prj:
        raise HTTPException(status_code=404, detail="Projeto nao encontrado.")
    if prj["status"] != "open":
        raise HTTPException(status_code=422, detail="Projeto nao esta aberto para captacao.")
    if payload.amount < prj["minimum_ticket"]:
        raise HTTPException(status_code=422, detail="Valor abaixo do ticket minimo.")

    uid = user.get("sub", "demo")
    wallet = _get_wallet(uid)
    if wallet["balance"] < payload.amount:
        raise HTTPException(status_code=422, detail="Saldo insuficiente na wallet interna.")

    wallet["balance"] = round(wallet["balance"] - payload.amount, 2)
    wallet["updated_at"] = datetime.now(timezone.utc).isoformat()
    prj["raised"] = round(prj["raised"] + payload.amount, 2)
    if prj["raised"] >= prj["target_raise"]:
        prj["status"] = "funded"

    oid = "MP" + secrets.token_hex(8).upper()
    MARKETPLACE_ORDERS[oid] = {
        "order_id": oid,
        "project_id": payload.project_id,
        "user_id": uid,
        "amount": payload.amount,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await _broadcast_wallet(uid)
    return {"order_id": oid, "project_id": payload.project_id, "wallet_balance": wallet["balance"]}


@app.get("/api/marketplace/orders")
def list_marketplace_orders(user: dict = Depends(get_current_user)) -> dict:
    uid = user.get("sub", "demo")
    items = [o for o in MARKETPLACE_ORDERS.values() if o["user_id"] == uid]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@app.websocket("/ws/market")
async def market_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            live_indicators = {
                "cdi": round(BASE_INDICATORS["cdi"] + random.uniform(-0.03, 0.03), 2),
                "selic": round(BASE_INDICATORS["selic"] + random.uniform(-0.02, 0.02), 2),
                "ipca": round(BASE_INDICATORS["ipca"] + random.uniform(-0.05, 0.05), 2),
                "tesouro_selic": round(BASE_INDICATORS["tesouro_selic"] + random.uniform(-0.04, 0.04), 2),
                "ibovespa": int(BASE_INDICATORS["ibovespa"] + random.uniform(-450, 450)),
                "dolar": round(BASE_INDICATORS["dolar"] + random.uniform(-0.04, 0.04), 2),
                "liquidez": BASE_INDICATORS["liquidez"],
            }
            await websocket.send_json(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "indicators": live_indicators,
                }
            )
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        return
