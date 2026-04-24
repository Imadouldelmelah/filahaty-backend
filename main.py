from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from utils.logger import logger
from routes import (
    prediction, ai_routes, news, 
    agronomy_routes, tracking_routes, agronomist_routes, 
    weather_routes, field_routes, marketplace_routes, unified_ai_routes,
    monitoring_routes, farming_routes
)

app = FastAPI()

# 1. Global Zero-Crash Middleware
@app.middleware("http")
async def safety_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"FATAL_UNHANDLED_EXCEPTION: {str(e)}")
        return JSONResponse(
            status_code=200,
            content={
                "status": "system_offline",
                "message": "Indestructible backend layer active. System is syncing.",
                "error": str(e)
            }
        )

# 2. Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"GLOBAL_EXCEPTION: {str(exc)}")
    return JSONResponse(
        status_code=200,
        content={"status": "error", "message": "Resilient baseline safe response."}
    )

# Include all active routers
app.include_router(ai_routes.router)
app.include_router(monitoring_routes.router)
app.include_router(prediction.router)
app.include_router(news.router)
app.include_router(agronomy_routes.router)
app.include_router(tracking_routes.router)
app.include_router(agronomist_routes.router)
app.include_router(weather_routes.router)
app.include_router(field_routes.router)
app.include_router(marketplace_routes.router)
app.include_router(unified_ai_routes.router)
app.include_router(farming_routes.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Filahaty Backend Active"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    # Run with detailed debug logging
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="debug")
