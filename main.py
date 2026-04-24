print("Starting backend...")

# Load .env FIRST before any other imports read env vars
from dotenv import load_dotenv
load_dotenv()


import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from utils.logger import logger

# Wrap risky imports to capture real crash reasons
try:
    from routes import (
        prediction, ai_routes, news, 
        agronomy_routes, tracking_routes, agronomist_routes, 
        weather_routes, field_routes, marketplace_routes, unified_ai_routes,
        monitoring_routes
    )
except Exception as e:
    print("Import error detected during startup:", str(e))
    # We don't raise here so the server can attempt to start in degraded mode
    prediction = ai_routes = news = agronomy_routes = \
    tracking_routes = agronomist_routes = weather_routes = \
    field_routes = marketplace_routes = unified_ai_routes = \
    monitoring_routes = None

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Optimized backend for crop recommendation and AI farming assistant.",
    version=settings.VERSION
)

# Setup CORS with restricted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware (metadata only for security)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate duration
    process_time = (time.time() - start_time) * 1000
    
    # Audit log (Internal context only, avoiding sensitive payload logging)
    logger.info(
        f"API_AUDIT: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Latency: {process_time:.2f}ms"
    )
    
    return response

# Include Routers with stability guard
try:
    if prediction: app.include_router(prediction.router)
    if ai_routes: app.include_router(ai_routes.router)
    if news: app.include_router(news.router)
    if agronomy_routes: app.include_router(agronomy_routes.router)
    if tracking_routes: app.include_router(tracking_routes.router)
    if agronomist_routes: app.include_router(agronomist_routes.router)
    if weather_routes: app.include_router(weather_routes.router)
    if field_routes: app.include_router(field_routes.router)
    if marketplace_routes: app.include_router(marketplace_routes.router)
    if unified_ai_routes: app.include_router(unified_ai_routes.router)
    if monitoring_routes: app.include_router(monitoring_routes.router)
except Exception as e:
    logger.error(f"STARTUP_ERROR: Failed to include some routers: {str(e)}")


@app.on_event("startup")
async def startup_event():
    import os
    # Verify critical settings on startup with explicit debug output
    # Verify critical settings on startup with explicit debug output
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"[STARTUP] OPENAI_API_KEY loaded: YES (length={len(api_key)})")
        logger.info("STARTUP: OPENAI_API_KEY is present and loaded.")
    else:
        print("[STARTUP] OPENAI_API_KEY loaded: NO — AI features will fail!")
        logger.error("STARTUP_ERROR: OPENAI_API_KEY is missing. Check .env or environment variables.")

    if not settings.NEWS_API_KEY:
        logger.warning("SECURITY_ALERT: NEWS_API_KEY is missing. News features will be disabled.")

    logger.info(f"Filahaty Backend Hardened Surface - v{settings.VERSION}")
    print("Server started successfully")

@app.get("/")
def root():
    return {
        "status": "Filahaty AI backend running",
        "security_level": "High"
    }

@app.get("/test")
def test_endpoint():
    return {"message": "ok"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/ai-test")
async def ai_test_endpoint():
    """
    Live OpenRouter connectivity test.
    """
    from services.deepseek_service import deepseek_svc
    try:
        # 1. Call OpenRouter with "hello"
        result = deepseek_svc.generate_reasoning("hello")
        
        # 2. Return result
        return {
            "status": "ok",
            "ai_response": result
        }
    except Exception as e:
        return {
            "status": "fail",
            "error": str(e)
        }

@app.get("/test-deepseek")
def test_deepseek():
    """
    Direct test for OpenRouter DeepSeek R1 integration.
    """
    try:
        from services.deepseek_service import deepseek_svc
        result = deepseek_svc.generate_reasoning("What are the best crops for dry soil?")
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-openai")
def test_openai():
    import os
    from openai import OpenAI
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("Missing OPENAI_API_KEY")
        client = OpenAI()
        
        print("Sending request to OpenAI...")
        # Note: Using the requested simplified API if supported on this test client
        response = client.responses.create(
            model="gpt-4.1-mini",
            input="Say hello"
        )
        
        return {"response": response.output_text}
        
    except Exception as e:
        print(f"OpenAI Test Error: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
