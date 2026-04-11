import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from utils.logger import logger

# Import routes
from routes import prediction, chat

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Filahaty Agricultural Platform API",
    description="Optimized backend for crop recommendation and AI farming assistant.",
    version="2.1.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(prediction.router)
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Filahaty Backend Starting Up - v2.1.0")

@app.get("/")
def root():
    return {
        "status": "Filahaty AI backend running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
