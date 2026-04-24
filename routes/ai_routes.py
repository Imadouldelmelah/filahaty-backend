from fastapi import APIRouter

router = APIRouter()


@router.post("/ai/chat")
def chat():
    return {"response": "AI working"}
