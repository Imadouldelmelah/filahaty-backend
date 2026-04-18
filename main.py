import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from utils.logger import logger

# Import routes
from routes import prediction, ai_routes, news, iot_routes, agronomy_routes, tracking_routes, agronomist_routes, weather_routes, field_routes, marketplace_routes, unified_ai_routes

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
    app.include_router(prediction.router)
    app.include_router(ai_routes.router)
    app.include_router(news.router)
    app.include_router(iot_routes.router)
    app.include_router(agronomy_routes.router)
    app.include_router(tracking_routes.router)
    app.include_router(agronomist_routes.router)
    app.include_router(weather_routes.router)
    app.include_router(field_routes.router)
    app.include_router(marketplace_routes.router)
    app.include_router(unified_ai_routes.router)
except Exception as e:
    logger.error(f"STARTUP_ERROR: Failed to include some routers: {str(e)}")


@app.on_event("startup")
async def startup_event():
    # Verify critical settings
    if not settings.OPENROUTER_API_KEY:
        logger.warning("SECURITY_ALERT: OPENROUTER_API_KEY is missing. AI features will fail.")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
