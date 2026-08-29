INTEGRATION

Put:
  index.html -> frontend/index.html
  login.html -> frontend/auth/login.html
  register.html -> frontend/auth/register.html
  auth.css -> frontend/auth/auth.css
  auth.js -> frontend/auth/auth.js

Your FastAPI main.py already serves frontend through /static, so the login URL is:
  http://127.0.0.1:8000/static/auth/login.html

Dashboard:
  http://127.0.0.1:8000/

Behavior:
- Logged out: Dashboard top-right shows Login / Register.
- Click opens the login page.
- Register creates a demo account and redirects to Dashboard.
- Login redirects to Dashboard.
- Dashboard then shows the user's name and a circular avatar containing the first character in uppercase.
- The name/avatar use the dashboard's existing theme variables and therefore change with Light/Dark/Ocean/Forest/Sunset.
- Clicking the logged-in name/avatar provides logout.
- Existing dashboard/API/analyzer/roadmap/library code is preserved.

This is frontend-only demo authentication. Do not use localStorage passwords in production; later connect the auth pages to FastAPI with hashed passwords and secure sessions/tokens.
