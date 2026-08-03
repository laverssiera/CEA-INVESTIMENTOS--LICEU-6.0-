from fastapi import APIRouter

from backend.app.federation.treasury_runtime.runtime import TreasuryRuntime
from backend.app.federation.underwriting.runtime import UnderwritingRuntime
from backend.app.federation.aml.runtime import AMLRuntime
from backend.app.federation.rwa_runtime.runtime import RWARuntime
from backend.app.federation.digital_twin.finance_twin import FinancialTwin
from backend.app.federation.interplanetary.runtime import InterplanetaryFinanceRuntime

router = APIRouter(
    prefix="/federation/finance",
    tags=["Federation Financial Runtime"]
)

@router.get("/treasury")
async def treasury():

    runtime = TreasuryRuntime()

    return runtime.liquidity_status()

@router.get("/underwriting")
async def underwriting():

    runtime = UnderwritingRuntime()

    return runtime.evaluate()

@router.get("/aml")
async def aml():

    runtime = AMLRuntime()

    return runtime.compliance_status()

@router.get("/rwa")
async def rwa():

    runtime = RWARuntime()

    return runtime.tokenized_assets()

@router.get("/twin")
async def finance_twin():

    twin = FinancialTwin()

    return twin.simulate()

@router.get("/interplanetary")
async def interplanetary():

    runtime = InterplanetaryFinanceRuntime()

    return runtime.orbital_market()
