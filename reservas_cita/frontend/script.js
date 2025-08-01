// ========================================
// Variables globales
// ========================================
const token = localStorage.getItem("token");

// ========================================
// Registro de Usuario
// ========================================
const registroForm = document.getElementById("registro-form");
if (registroForm) {
  registroForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nombre = document.getElementById("reg-nombre").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-pass").value;

    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, email, password }),
      });

      if (response.ok) {
        alert("✅ Registro exitoso. Ahora inicia sesión.");
        registroForm.reset();
        window.location.href = "login.html";
      } else {
        const error = await response.json();
        console.error("Registro - Error del backend:", error);
        alert("❌ Error al registrar: " + (error.detail || JSON.stringify(error)));
      }
    } catch (err) {
      console.error("Registro - Error de red:", err);
      alert("❌ Error de red");
    }
  });
}

// ========================================
// Inicio de Sesión
// ========================================
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-pass").value;

    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        alert("✅ Inicio de sesión exitoso");
        window.location.href = "index.html";
      } else {
        alert("❌ Credenciales inválidas");
      }
    } catch (err) {
      console.error("Login - Error de red:", err);
      alert("❌ Error de red");
    }
  });
}

// ========================================
// Página Principal - index.html
// ========================================
if (window.location.pathname.includes("index.html")) {
  if (!token) {
    window.location.href = "login.html";
  } else {
    fetch("http://localhost:8000/users/me", {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
      .then((res) => res.json())
      .then((user) => {
        const userInfo = document.getElementById("user-info");
        if (userInfo) {
          userInfo.innerText = `👋 Hola, ${user.nombre || user.email}`;
        }
      })
      .catch((err) => {
        console.error("Error al cargar usuario:", err);
        document.getElementById("user-info").innerText = "Error al obtener usuario";
      });
  }
}

// ========================================
// Agendar Cita
// ========================================
const citaForm = document.getElementById("cita-form");
if (citaForm) {
  if (!token) {
    alert("🔒 Debes iniciar sesión para agendar una cita");
    window.location.href = "login.html";
  } else {
    citaForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const fecha = document.getElementById("fecha").value;
      const servicio = document.getElementById("servicio").value;

      try {
        const response = await fetch("http://localhost:8000/citas/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          body: JSON.stringify({ fecha_hora: fecha, servicio }),
        });

        if (response.ok) {
          alert("✅ Cita agendada correctamente");
          citaForm.reset();
        } else {
          const error = await response.json();
          alert("❌ Error: " + (error.detail || "No se pudo agendar"));
        }
      } catch (err) {
        console.error("Agendar cita - Error:", err);
        alert("❌ Error de red");
      }
    });
  }
}

// ========================================
// Cerrar Sesión
// ========================================
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    alert("🔒 Sesión cerrada");
    window.location.href = "login.html";
  });
}
