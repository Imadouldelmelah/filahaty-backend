import time
from fastapi import APIRouter, HTTPException
from models.chat_models import ChatRequest, ChatResponse
from services.gemini_service import GeminiService
from utils.logger import logger

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

# Initialize service safely
try:
    gemini_service = GeminiService()
except Exception as e:
    logger.critical(f"FATAL: GeminiService failed to initialize: {e}")
    gemini_service = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    # Log incoming user message
    print("User message received:", request.message)
    
    if not gemini_service:
        logger.error("Chat request rejected: GeminiService unavailable")
        raise HTTPException(status_code=503, detail="AI Service is currently offline")
        
    start_time = time.time()
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Call the GeminiService to generate the AI reply
        # Improved GeminiService now handles model fallback internally
        response_text = await gemini_service.generate_response(request.message)
        
        duration = time.time() - start_time
        logger.info(f"Chat Request Handled: status=200, duration={duration:.2f}s")
        
        # Return JSON: {"response": "AI response text"}
        return ChatResponse(response=response_text)
        
    except Exception as e:
        # Proper error handling and logging
        logger.error(f"AI Routes Error: {str(e)}", exc_info=True)
        print("AI assistant route error:", e)
        raise HTTPException(status_code=500, detail=f"AI assistant error: {str(e)}")
