from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes import router


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE = Path(__file__).resolve().parents[1]
FRONTEND = BASE / "frontend"
AUTH_DIR = FRONTEND / "auth"


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Skill Gap Analyzer",
    version="1.0.0"
)


# ---------------------------------------------------------
# Existing API routes
# ---------------------------------------------------------

app.include_router(router, prefix="/api")


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

@app.get("/")
def dashboard():
    return FileResponse(FRONTEND / "index.html")


# ---------------------------------------------------------
# Roadmap
# ---------------------------------------------------------

@app.get("/roadmap.html")
def roadmap_page():
    return FileResponse(FRONTEND / "roadmap.html")


# ---------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------

@app.get("/auth/login", include_in_schema=False)
def auth_login():
    return FileResponse(AUTH_DIR / "login.html")


# Support direct .html URL too
@app.get("/auth/login.html", include_in_schema=False)
def auth_login_html():
    return FileResponse(AUTH_DIR / "login.html")


# ---------------------------------------------------------
# REGISTER PAGE
# ---------------------------------------------------------

@app.get("/auth/register", include_in_schema=False)
def auth_register():
    return FileResponse(AUTH_DIR / "register.html")


# Support direct .html URL too
@app.get("/auth/register.html", include_in_schema=False)
def auth_register_html():
    return FileResponse(AUTH_DIR / "register.html")


# ---------------------------------------------------------
# AUTH CSS
# ---------------------------------------------------------

@app.get("/auth/auth.css", include_in_schema=False)
def auth_css():
    return FileResponse(
        AUTH_DIR / "auth.css",
        media_type="text/css"
    )


# ---------------------------------------------------------
# AUTH JAVASCRIPT
# ---------------------------------------------------------

@app.get("/auth/auth.js", include_in_schema=False)
def auth_js():
    return FileResponse(
        AUTH_DIR / "auth.js",
        media_type="application/javascript"
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}