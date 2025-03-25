from fastapi import APIRouter
from app.api.api_v1.endpoints import simulations, scenarios

router = APIRouter()
router.include_router(simulations.router, prefix="/simulations", tags=["simulations"])
router.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
