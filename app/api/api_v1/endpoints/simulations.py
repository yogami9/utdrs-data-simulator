from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import random

from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

class SimulationRequest(BaseModel):
    scenarios: Optional[List[str]] = None
    duration: Optional[int] = None  # in seconds
    intensity: Optional[str] = "medium"  # low, medium, high

# In-memory simulation tracking for demo purposes
# In a real app, this would be stored in MongoDB
SIMULATIONS = {}

@router.post("/start")
async def start_simulation(request: SimulationRequest, background_tasks: BackgroundTasks):
    """Start a simulation with specified scenarios."""
    # Generate simulation ID
    simulation_id = str(uuid.uuid4())
    
    # Default scenarios if none provided
    scenarios = request.scenarios or ["phishing", "data_exfiltration"]
    
    # Record simulation start
    start_time = datetime.utcnow()
    SIMULATIONS[simulation_id] = {
        "id": simulation_id,
        "scenarios": scenarios,
        "intensity": request.intensity or "medium",
        "duration": request.duration,
        "start_time": start_time,
        "status": "running"
    }
    
    # For demo purposes, update status after a short delay
    # In a real app, this would actually run the scenarios
    background_tasks.add_task(
        _update_simulation_status, 
        simulation_id=simulation_id
    )
    
    return {
        "simulation_id": simulation_id,
        "message": f"Simulation started with {len(scenarios)} scenarios",
        "scenarios": scenarios,
        "start_time": start_time
    }

@router.post("/stop")
async def stop_simulation():
    """Stop all running simulations."""
    stopped_count = 0
    
    for sim_id, simulation in SIMULATIONS.items():
        if simulation["status"] == "running":
            simulation["status"] = "stopped"
            simulation["end_time"] = datetime.utcnow()
            stopped_count += 1
    
    return {
        "message": f"Stopped {stopped_count} running simulations",
        "stopped_count": stopped_count
    }

@router.get("/status")
async def get_simulation_status():
    """Get the current status of simulations."""
    running = [s for s in SIMULATIONS.values() if s["status"] == "running"]
    completed = [s for s in SIMULATIONS.values() if s["status"] == "completed"]
    
    return {
        "running_count": len(running),
        "running": running,
        "completed_count": len(completed),
        "recently_completed": completed[-5:] if completed else []
    }

@router.post("/trigger/{scenario_id}")
async def trigger_scenario(scenario_id: str, background_tasks: BackgroundTasks):
    """Trigger a specific scenario immediately."""
    # Check if scenario exists
    valid_scenarios = ["phishing", "ransomware", "data_exfiltration", "brute_force", "insider_threat"]
    if scenario_id not in valid_scenarios:
        raise HTTPException(status_code=404, detail=f"Scenario {scenario_id} not found")
    
    # Generate trigger ID
    trigger_id = str(uuid.uuid4())
    
    return {
        "trigger_id": trigger_id,
        "scenario_id": scenario_id,
        "message": f"Scenario {scenario_id} triggered",
        "trigger_time": datetime.utcnow()
    }

# Background task to simulate running scenarios
async def _update_simulation_status(simulation_id: str):
    """Update simulation status after a delay (simulating execution)."""
    import asyncio
    
    # Wait for a random amount of time (3-10 seconds)
    await asyncio.sleep(random.uniform(3, 10))
    
    # Update simulation status
    if simulation_id in SIMULATIONS:
        SIMULATIONS[simulation_id]["status"] = "completed"
        SIMULATIONS[simulation_id]["end_time"] = datetime.utcnow()
        logger.info(f"Simulation {simulation_id} completed")
