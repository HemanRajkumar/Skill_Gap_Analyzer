# Skill Gap Analyzer - Login/Register pages

## Files
- `login.html` - login page
- `register.html` - registration page
- `auth.css` - shared styling
- `auth.js` - theme + demo authentication logic

## Run now
These pages work without changing your existing FastAPI project.

From the project root, copy these files into:
`frontend/auth/`

Then open:
`http://127.0.0.1:8000/static/auth/login.html`

Or, if your FastAPI static mount serves the frontend directory, use:
`http://127.0.0.1:8000/static/auth/register.html`

## What works now
- Login/register page UI
- Light, Dark, System themes
- System is the default theme
- Theme choice is saved in localStorage
- Password show/hide
- Registration validation
- Demo account stored locally in browser localStorage
- Login checks the locally-created account
- Successful login redirects to the existing `frontend/index.html`
- No changes are made to your existing analyzer, roadmap, skill matcher, RAG, or Chroma code.

## Important
This is intentionally a frontend-only authentication prototype.

Do NOT use localStorage passwords for a real deployed application. Later, replace the demo logic with FastAPI authentication and hashed passwords/database storage.

## Planned integration structure
frontend/
  index.html
  roadmap.html
  auth/
    login.html
    register.html
    auth.css
    auth.js

Later backend:
app/
  api/
    auth_routes.py
  models/
    auth_schemas.py
  services/
    auth_service.py

Future user area:
- Profile / user details
- Saved roadmaps
- Separate Analyze search/workspace
- Dashboard
- Skills Library
- Roadmap history
