
(function () {
  const THEME_KEY = "skillGapTheme";
  const USERS_KEY = "skillGapUsers";

  function getTheme() {
    return localStorage.getItem(THEME_KEY) || "system";
  }

  function applyTheme(theme) {
    document.body.classList.remove("light", "dark", "system");
    document.body.classList.add(theme);

    document.querySelectorAll("[data-theme-choice]").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.themeChoice === theme);
    });

    localStorage.setItem(THEME_KEY, theme);
  }

  applyTheme(getTheme());

  document.querySelectorAll("[data-theme-choice]").forEach(btn => {
    btn.addEventListener("click", () => {
      applyTheme(btn.dataset.themeChoice);
    });
  });

  document.querySelectorAll("[data-toggle-password]").forEach(btn => {
    btn.addEventListener("click", () => {
      const input = document.getElementById(btn.dataset.togglePassword);

      if (!input) return;

      if (input.type === "password") {
        input.type = "text";
        btn.textContent = "◎";
        btn.setAttribute("aria-label", "Hide password");
      } else {
        input.type = "password";
        btn.textContent = "◉";
        btn.setAttribute("aria-label", "Show password");
      }
    });
  });

  function getUsers() {
    try {
      return JSON.parse(localStorage.getItem(USERS_KEY) || "[]");
    } catch {
      return [];
    }
  }

  function saveUsers(list) {
    localStorage.setItem(USERS_KEY, JSON.stringify(list));
  }

  function showMessage(text, type = "") {
    const el = document.getElementById("authMessage");

    if (!el) return;

    el.textContent = text;
    el.className = "auth-message " + type;
  }

  function clearMessage() {
    const el = document.getElementById("authMessage");

    if (!el) return;

    el.textContent = "";
    el.className = "auth-message";
  }

  /* =========================================================
     LOGIN
     ========================================================= */

  const loginForm = document.getElementById("loginForm");

  if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
      event.preventDefault();
      clearMessage();

      const emailInput = document.getElementById("loginEmail");
      const passwordInput = document.getElementById("loginPassword");

      const email = emailInput.value.trim().toLowerCase();
      const password = passwordInput.value;

      if (!email || !password) {
        showMessage(
          "Please enter your email address and password.",
          "error"
        );
        return;
      }

      const users = getUsers();

      const user = users.find(
        item => item.email === email
      );

      /*
       * IMPORTANT:
       * Check the email first and password separately.
       * This allows the user to see a clear error on screen.
       */

      if (!user) {
        showMessage(
          "No account was found with this email address. Please create an account first.",
          "error"
        );
        emailInput.focus();
        return;
      }

      if (user.password !== password) {
        showMessage(
          "Incorrect password. Please try again or use Forgot password.",
          "error"
        );
        passwordInput.value = "";
        passwordInput.focus();
        return;
      }

      localStorage.setItem(
        "skillGapCurrentUser",
        JSON.stringify({
          name: user.name,
          email: user.email
        })
      );

      showMessage(
        "Login successful. Opening your dashboard...",
        "success"
      );

      setTimeout(() => {
        window.location.href = "/";
      }, 600);
    });

    /* =======================================================
       FORGOT PASSWORD
       ======================================================= */

    const forgotPassword = document.getElementById("forgotPassword");
    const resetBox = document.getElementById("resetBox");
    const resetForm = document.getElementById("resetForm");
    const cancelReset = document.getElementById("cancelReset");

    if (forgotPassword && resetBox) {
      forgotPassword.addEventListener("click", function (event) {
        event.preventDefault();

        clearMessage();

        resetBox.hidden = false;

        const resetEmail = document.getElementById("resetEmail");

        if (resetEmail) {
          resetEmail.value =
            document.getElementById("loginEmail")?.value.trim() || "";

          setTimeout(() => {
            resetEmail.focus();
          }, 50);
        }
      });
    }

    if (cancelReset && resetBox) {
      cancelReset.addEventListener("click", function () {
        resetBox.hidden = true;
        clearMessage();
      });
    }

    if (resetForm) {
      resetForm.addEventListener("submit", function (event) {
        event.preventDefault();
        clearMessage();

        const email =
          document.getElementById("resetEmail").value.trim().toLowerCase();

        const newPassword =
          document.getElementById("resetNewPassword").value;

        const confirmPassword =
          document.getElementById("resetConfirmPassword").value;

        if (!email) {
          showMessage(
            "Please enter the email address used for your account.",
            "error"
          );
          return;
        }

        if (newPassword.length < 8) {
          showMessage(
            "New password must be at least 8 characters.",
            "error"
          );
          return;
        }

        if (newPassword !== confirmPassword) {
          showMessage(
            "The new passwords do not match.",
            "error"
          );
          return;
        }

        const users = getUsers();

        const userIndex = users.findIndex(
          item => item.email === email
        );

        if (userIndex === -1) {
          showMessage(
            "No account was found with this email address.",
            "error"
          );
          return;
        }

        /*
         * Frontend prototype:
         * update the demo account stored in localStorage.
         *
         * In production this must be replaced by a
         * backend password-reset flow with a secure token.
         */

        users[userIndex].password = newPassword;
        saveUsers(users);

        resetBox.hidden = true;

        document.getElementById("loginEmail").value = email;
        document.getElementById("loginPassword").value = "";

        showMessage(
          "Password reset successfully. You can now log in with your new password.",
          "success"
        );
      });
    }

    /* =======================================================
       GOOGLE BUTTON
       ======================================================= */

    document.getElementById("googleDemo")?.addEventListener("click", () => {
      showMessage(
        "Google sign-in needs Google OAuth configuration. The button is ready for later backend integration.",
        "error"
      );
    });
  }

  /* =========================================================
     REGISTER
     ========================================================= */

  const registerForm = document.getElementById("registerForm");

  if (registerForm) {
    const password = document.getElementById("registerPassword");
    const meter = document.querySelectorAll(".password-meter i");

    password?.addEventListener("input", () => {
      const length = password.value.length;

      meter.forEach((bar, index) => {
        bar.classList.toggle(
          "on",
          length >= (index + 1) * 3
        );
      });
    });

    registerForm.addEventListener("submit", function (event) {
      event.preventDefault();
      clearMessage();

      const name =
        document.getElementById("registerName").value.trim();

      const email =
        document.getElementById("registerEmail").value.trim().toLowerCase();

      const pass =
        document.getElementById("registerPassword").value;

      const confirm =
        document.getElementById("confirmPassword").value;

      const agree =
        document.getElementById("agreeTerms").checked;

      if (!name || !email || !pass || !confirm) {
        showMessage(
          "Please fill in all fields.",
          "error"
        );
        return;
      }

      if (pass.length < 8) {
        showMessage(
          "Password must be at least 8 characters.",
          "error"
        );
        return;
      }

      if (pass !== confirm) {
        showMessage(
          "Passwords do not match.",
          "error"
        );
        return;
      }

      if (!agree) {
        showMessage(
          "Please accept the Terms of Service and Privacy Policy.",
          "error"
        );
        return;
      }

      const users = getUsers();

      if (users.some(user => user.email === email)) {
        showMessage(
          "An account with this email already exists. Please log in.",
          "error"
        );
        return;
      }

      users.push({
        name: name,
        email: email,
        password: pass
      });

      saveUsers(users);

      localStorage.setItem(
        "skillGapCurrentUser",
        JSON.stringify({
          name: name,
          email: email
        })
      );

      showMessage(
        "Account created successfully. Opening your dashboard...",
        "success"
      );

      setTimeout(() => {
        window.location.href = "/";
      }, 600);
    });

    document.getElementById("googleDemo")?.addEventListener("click", () => {
      showMessage(
        "Google sign-up needs Google OAuth configuration. The button is ready for later backend integration.",
        "error"
      );
    });
  }
})();
