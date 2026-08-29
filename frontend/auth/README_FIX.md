# Fixed Login

Replace only these files in your existing `frontend/auth/` folder:

- login.html
- auth.js

Keep your existing `auth.css`.

Fixes:
1. Wrong password is shown clearly on the login screen.
2. Unknown email is shown clearly on the login screen.
3. Forgot password opens an on-screen reset form.
4. Reset validates the email and new password.
5. Reset updates the demo account and lets the user log in with the new password.
6. No existing analyzer/roadmap/backend files are changed.

Important: this is still frontend-only demo authentication. A production reset flow must use a secure backend reset token and hashed passwords.
