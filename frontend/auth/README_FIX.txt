INTEGRATED INDEX + AUTH FIX

1. Put index.html in frontend/index.html. This is the user's supplied index.html with only auth/header integration added; the dashboard pages, API calls, themes, skill analysis and roadmap code are preserved.
2. Put login.html, register.html, auth.css and auth.js in frontend/auth/.
3. Add the routes in main_auth_routes.py to your existing app/main.py. Do NOT replace app/main.py.
4. The dashboard Login / Register button opens /auth/login.
5. After successful login/register, auth.js stores skillGapCurrentUser and redirects to /.
6. The dashboard then shows the user's name and a circular first-capital-letter avatar.
7. Login/auth pages and dashboard now share localStorage key skillGapTheme so theme selection stays synchronized.
8. The Pro Tip block is not present in this index.
9. Restart: python -m uvicorn app.main:app --reload
10. Open http://127.0.0.1:8000/

If you still see GET /static/auth/login.html 404, do not use that old URL. The integrated index uses /auth/login, and the FastAPI routes above must be present.
