from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.routes import router
BASE=Path(__file__).resolve().parents[1]; FRONTEND=BASE/"frontend"
app=FastAPI(title="Skill Gap Analyzer",version="1.0.0")
app.include_router(router,prefix="/api")
@app.get("/")
def dashboard(): return FileResponse(FRONTEND/"index.html")
@app.get("/roadmap.html")
def roadmap_page(): return FileResponse(FRONTEND/"roadmap.html")
@app.get("/health")
def health(): return {"status":"ok"}
