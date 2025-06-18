document.addEventListener('DOMContentLoaded', function() {
  const nombresCientificos = {
    "Álamo": "Populus alba",
    "Ahuehuete": "Taxodium mucronatum",
    "Ahuejote": "Salix bonplandiana",
    "Aile": "Alnus acuminata",
    "Árbol de Fuego": "Delonix regia",
    "Árbol de Judas": "Cercis siliquastrum",
    "Árbol Lluvia de Oro": "Cassia fistula",
    "Árbol de la Llama": "Brachychiton acerifolius",
    "Árbol del Paraíso": "Melia azedarach",
    "Avellano": "Corylus avellana",
    "Bugambilia": "Bougainvillea glabra",
    "Cacalosúchil": "Plumeria rubra",
    "Caoba": "Swietenia macrophylla",
    "Capulín": "Prunus salicifolia",
    "Casuarina": "Casuarina equisetifolia",
    "Cedro Blanco": "Cupressus lusitanica",
    "Cedro Rojo": "Cedrela odorata",
    "Ceiba": "Ceiba pentandra",
    "Ciprés": "Cupressus sempervirens",
    "Encino": "Quercus robur",
    "Eucalipto": "Eucalyptus globulus",
    "Fresno": "Fraxinus uhdei",
    "Guayabo": "Psidium guajava",
    "Jacaranda": "Jacaranda mimosifolia",
    "Laurel de la India": "Ficus benjamina",
    "Liquidámbar": "Liquidambar styraciflua",
    "Magnolia": "Magnolia grandiflora",
    "Mezquite": "Prosopis laevigata",
    "Naranjo": "Citrus sinensis",
    "Níspero": "Eriobotrya japonica",
    "Olmo": "Ulmus pumila",
    "Pino": "Pinus cembroides",
    "Pirul": "Schinus molle",
    "Roble": "Quercus rugosa",
    "Sauce Llorón": "Salix babylonica",
    "Tabachín": "Caesalpinia pulcherrima",
    "Tecoma": "Tecoma stans",
    "Tejocote": "Crataegus mexicana",
    "Tzalam": "Lysiloma latisiliquum",
    "Tulipán Africano": "Spathodea campanulata",
    "Tule": "Taxodium distichum",
    "Yuca": "Yucca elephantipes",
    "Zapote Blanco": "Casimiroa edulis",
    "Zapote Negro": "Diospyros digyna",
    "Otro": "Desconocido"
  };

  function actualizarNombreCientifico() {
    const selectArbol = document.getElementById('nombre_comun');
    const inputCientifico = document.getElementById('nombre_cientifico_input');
    const arbolSeleccionado = selectArbol.value;
    
    if (arbolSeleccionado && nombresCientificos[arbolSeleccionado]) {
      inputCientifico.value = nombresCientificos[arbolSeleccionado];
    } else {
      inputCientifico.value = "";
    }
  }

  // Actualizar nombre científico cuando cambie el select
  const selectArbol = document.getElementById('nombre_comun');
  selectArbol.addEventListener('change', actualizarNombreCientifico);
  actualizarNombreCientifico(); // Para setear al cargar la página si ya tiene valor

  // Fecha actual para el campo de fecha_registro
  const now = new Date();
  const fechaActual = now.toISOString().split('T')[0];
  const fechaRegistroInput = document.getElementById('fecha_registro');
  if(fechaRegistroInput) {
    fechaRegistroInput.value = fechaActual;
  }

  // Mostrar/ocultar campo "Otro" en ubicación
  const ubicacionSelect = document.getElementById('ubicacionSelect');
  const ubicacionOtroContainer = document.getElementById('ubicacionOtroContainer');
  if(ubicacionSelect && ubicacionOtroContainer) {
    ubicacionSelect.addEventListener('change', function() {
      if (this.value === 'Otro') {
        ubicacionOtroContainer.classList.remove('hidden');
        document.getElementById('ubicacionOtroInput').required = true;
      } else {
        ubicacionOtroContainer.classList.add('hidden');
        const otroInput = document.getElementById('ubicacionOtroInput');
        otroInput.required = false;
        otroInput.value = '';
      }
    });
  }

  // Previsualización de fotos
  for (let i = 1; i <= 5; i++) {
    const input = document.getElementById(`foto${i}`);
    const preview = document.getElementById(`preview${i}`);
    if (input && preview) {
      input.addEventListener('change', function() {
        if (this.files && this.files[0]) {
          const reader = new FileReader();
          reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
          }
          reader.readAsDataURL(this.files[0]);
        }
      });
    }
  }

  // Validación de altura máxima 50 metros en formulario
  const arbolForm = document.getElementById('arbolForm');
  if (arbolForm) {
    arbolForm.addEventListener('submit', function(event) {
      const alturaInput = document.getElementById('altura');
      if (alturaInput && alturaInput.value > 50) {
        alert("La altura no puede ser mayor a 50 metros.");
        event.preventDefault();
        return;
      }
      // Aquí va la lógica de envío por fetch (si quieres hacer fetch)
      event.preventDefault(); // Evitar envío por defecto para manejar fetch

      const formData = new FormData(arbolForm);

      fetch(arbolForm.action, {
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
          document.getElementById('successModal').classList.remove('hidden');
          setTimeout(() => {
            window.location.href = data.redirect_url;
          }, 2000);
        } else {
          alert('Error: ' + (data.error || 'Datos inválidos'));
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error al conectar con el servidor');
      });
    });
  }

  // Mostrar modal de éxito si viene en URL
  const urlParams = new URLSearchParams(window.location.search);
  const success = urlParams.get('success');
  if (success === 'true') {
    const modal = document.getElementById('successModal');
    if(modal) {
      modal.classList.remove('hidden');
    }
  }

  // Botón para cerrar modal y redirigir
  const modalOkButton = document.getElementById('modalOkButton');
  if (modalOkButton) {
    modalOkButton.addEventListener('click', function() {
      window.location.href = "{% url 'arbol:inicio' %}";
    });
  }

  // Listener para validar e intentar formatear inclinación del tronco
  const inclinacionInput = document.getElementById('inclinacion_tronco');
  if(inclinacionInput) {
    inclinacionInput.addEventListener('input', function(event) {
      let input = event.target.value;
      // Regex para aceptar hasta 3 dígitos para grados, 2 para minutos y segundos con símbolos
      let regex = /^(\d{0,3})°\s*(\d{0,2})'\s*(\d{0,2})"&/;
      if (regex.test(input)) {
        input = input.replace(regex, '$1° $2\' $3"&');
      } else {
        input = input.replace(/[^0-9°'\s"]/g, '');
      }
      event.target.value = input;
    });
  }
});
