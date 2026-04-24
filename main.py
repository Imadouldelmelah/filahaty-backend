from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    # Run with detailed debug logging
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="debug")
