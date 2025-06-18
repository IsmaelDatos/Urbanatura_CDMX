// Funciones para los toggle switches
function toggleRegisterType(type) {
  const personTab = document.getElementById('person-tab');
  const institutionTab = document.getElementById('institution-tab');
  const personForm = document.getElementById('person-form');
  const institutionForm = document.getElementById('institution-form');

  if (type === 'person') {
    personTab.classList.add('active');
    institutionTab.classList.remove('active');
    personForm.classList.remove('hidden');
    institutionForm.classList.add('hidden');
  } else {
    personTab.classList.remove('active');
    institutionTab.classList.add('active');
    personForm.classList.add('hidden');
    institutionForm.classList.remove('hidden');
  }
}

function submitForm(form) {
  const formData = new FormData(form);
  
  // Limpiar errores previos
  document.querySelectorAll('.error-message').forEach(el => {
    el.classList.add('hidden');
    el.textContent = '';
  });
  
  fetch(form.action, {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = data.redirect_url || "/arbol/inicio/";
    } else {
      // Mostrar errores de validación
      if (data.errors) {
        for (const [field, error] of Object.entries(data.errors)) {
          const errorElement = document.getElementById(`${form.id}-${field}-error`) || 
                             document.getElementById(`${field}-error`);
          if (errorElement) {
            errorElement.textContent = error;
            errorElement.classList.remove('hidden');
          } else {
            console.error(`No se encontró elemento para error: ${field}`);
          }
        }
      } else {
        alert('Error: ' + (data.error || 'Datos inválidos'));
      }
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error al conectar con el servidor');
  });
}

// Configuración del envío de formularios
document.addEventListener('DOMContentLoaded', function() {
  // Configuración para el formulario de persona
  const personForm = document.getElementById('person-form');
  if (personForm) {
    personForm.addEventListener('submit', function(e) {
      e.preventDefault();
      submitForm(personForm);
    });
  }

  // Configuración para el formulario de institución
  const institutionForm = document.getElementById('institution-form');
  if (institutionForm) {
    institutionForm.addEventListener('submit', function(e) {
      e.preventDefault();
      submitForm(institutionForm);
    });
  }
});