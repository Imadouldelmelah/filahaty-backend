from fastapi import APIRouter

router = APIRouter()

@router.post("/ai/chat")
def chat():
    return {"response": "AI working"}

@router.get("/monitoring/fake")
def fake():
    return {
        "temperature": 25,
        "humidity": 60,
        "soil_moisture": 40
    }
