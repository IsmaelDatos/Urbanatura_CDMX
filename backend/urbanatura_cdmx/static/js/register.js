// --- VALIDACIÓN DE CONTRASEÑAS ---
function verificarPasswords(form) {
  const formId = form.id;
  const password1 = form.password1;
  const password2 = form.password2;
  const errorField = formId === "person-form" ? "password2" : "institution-password2";
  let errorElement = document.getElementById(`${errorField}-error`);

  // Elimina errores previos si existen y las contraseñas ahora coinciden
  if (password1.value === password2.value) {
    if (errorElement) {
      errorElement.classList.add("hidden");
    }
    password1.classList.remove("border-red-500");
    password2.classList.remove("border-red-500");
    return true;
  }

  // Si no coinciden, muestra el error
  if (!errorElement) {
    errorElement = document.createElement("div");
    errorElement.id = `${errorField}-error`;
    errorElement.className = "error-message text-red-500 text-xs mt-1 flex items-center";
    errorElement.innerHTML =
      `<i class="fas fa-exclamation-circle mr-1"></i><span>Las contraseñas no coinciden</span>`;
    password2.parentNode.appendChild(errorElement);
  } else {
    errorElement.classList.remove("hidden");
    errorElement.innerHTML =
      `<i class="fas fa-exclamation-circle mr-1"></i><span>Las contraseñas no coinciden</span>`;
  }

  password1.classList.add("border-red-500");
  password2.classList.add("border-red-500");
  return false;
}

// --- OJITO PARA MOSTRAR/OCULTAR CONTRASEÑA ---
function togglePasswordVisibility(btn, inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === "password") {
    input.type = "text";
    btn.classList.remove("fa-eye");
    btn.classList.add("fa-eye-slash");
  } else {
    input.type = "password";
    btn.classList.remove("fa-eye-slash");
    btn.classList.add("fa-eye");
  }
}

// --- EVENTOS PARA VALIDACIÓN EN TIEMPO REAL ---
document.addEventListener("DOMContentLoaded", () => {
  ["person-form", "institution-form"].forEach(formId => {
    const form = document.getElementById(formId);
    if (form) {
      form.password1.addEventListener("input", () => verificarPasswords(form));
      form.password2.addEventListener("input", () => verificarPasswords(form));
      form.addEventListener("submit", function(e) {
        if (!verificarPasswords(form)) {
          e.preventDefault();
        } else {
          const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
          const formData = new FormData(form);
          formData.append('csrfmiddlewaretoken', csrfToken);
        }
      });
    }
  });
});