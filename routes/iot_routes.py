from fastapi import APIRouter
import random

router = APIRouter(tags=["IoT Simulation"])

@router.get("/iot/data")
def get_iot_data():
    """
    Returns simulated real-time IoT sensor data from the field.
    Provides N, P, K, and environmental metrics for crop recommendation.
    """
    return {
        "N": random.randint(50, 100),
        "P": random.randint(30, 60),
        "K": random.randint(20, 50),
        "temperature": round(random.uniform(15.0, 35.0), 1),
        "humidity": round(random.uniform(40.0, 90.0), 1),
        "ph": round(random.uniform(5.5, 7.5), 1),
        "rainfall": round(random.uniform(0.0, 200.0), 1)
    }
