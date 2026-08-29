# Add these routes to your EXISTING app/main.py. Do not replace your existing API routes.
from pathlib import Path
from fastapi.responses import FileResponse

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
AUTH_DIR = FRONTEND_DIR / "auth"

@app.get("/auth/login", include_in_schema=False)
def auth_login():
    return FileResponse(AUTH_DIR / "login.html")

@app.get("/auth/register", include_in_schema=False)
def auth_register():
    return FileResponse(AUTH_DIR / "register.html")

@app.get("/auth/auth.css", include_in_schema=False)
def auth_css():
    return FileResponse(AUTH_DIR / "auth.css", media_type="text/css")

@app.get("/auth/auth.js", include_in_schema=False)
def auth_js():
    return FileResponse(AUTH_DIR / "auth.js", media_type="application/javascript")
