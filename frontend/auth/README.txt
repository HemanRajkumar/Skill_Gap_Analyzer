FIXED INTEGRATION

Replace only:
frontend/index.html
frontend/auth/login.html
frontend/auth/register.html
frontend/auth/auth.css
frontend/auth/auth.js

Run:
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/

Important:
- Do NOT use Live Server for this project.
- Use FastAPI/Uvicorn because index.html calls /api/roles, /api/analyze, /api/roadmap, /api/skills and /api/skill-analyze.
- Logged out dashboard: Login / Register.
- Logged in dashboard: first letter + username.
- Existing dashboard theme controls remain the same.
- Username/profile uses the dashboard's existing theme variables.
- The old top-right sun button/avatar is removed.
- Existing analyzer, roadmap, skill library and API code is preserved.
