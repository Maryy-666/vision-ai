from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI()

FRONTEND_DIR = Path(__file__).parent
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")
app.include_router(router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
async def health():
    return {
        "status": "healthy"
    }