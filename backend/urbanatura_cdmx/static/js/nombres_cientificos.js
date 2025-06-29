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
  const selectArbol = document.getElementById('nombre_comun');
  selectArbol.addEventListener('change', actualizarNombreCientifico);
  actualizarNombreCientifico();
  const now = new Date();
  const fechaActual = now.toISOString().split('T')[0];
  const fechaRegistroInput = document.getElementById('fecha_registro');
  if(fechaRegistroInput) {
    fechaRegistroInput.value = fechaActual;
  }
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
  const urlParams = new URLSearchParams(window.location.search);
  const success = urlParams.get('success');
  if (success === 'true') {
    const modal = document.getElementById('successModal');
    if(modal) {
      modal.classList.remove('hidden');
    }
  }
  const modalOkButton = document.getElementById('modalOkButton');
  if (modalOkButton) {
    modalOkButton.addEventListener('click', function() {
      const inicioUrl = this.getAttribute('data-inicio-url');
      window.location.href = inicioUrl;
    });
  }
  const inclinacionInput = document.getElementById('inclinacion_tronco');
  if(inclinacionInput) {
    inclinacionInput.addEventListener('input', function(event) {
      let input = event.target.value;
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
