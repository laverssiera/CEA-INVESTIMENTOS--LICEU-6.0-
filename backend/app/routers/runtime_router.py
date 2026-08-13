from fastapi import APIRouter
from app.runtime.twin.economic_twin import twin
from app.runtime.causal_engine.runtime import runtime

router = APIRouter(prefix="/runtime")

@router.get("/economic-twin")
def economic_twin():
    return twin.simulate_crisis()

@router.get("/causal-risk")
def causal_risk():

    return {
        "status": runtime.evaluate(
            80,
            60,
            40
        )
    }
