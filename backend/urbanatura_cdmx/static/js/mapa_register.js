// mapa_register.js - Versión mejorada con autocompletado de CP

// Variables globales
let currentFormType = 'person';
let map = null;
let marker = null;
let cpCache = {};

// Inicializar el mapa
function initMap() {
    // Coordenadas iniciales (Centro de CDMX)
    const initialCoords = [19.4326, -99.1332];
    
    // Crear el mapa
    map = L.map('map').setView(initialCoords, 13);
    
    // Añadir capa de tiles (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Crear marcador inicial
    marker = L.marker(initialCoords, {
        draggable: true,
        autoPan: true
    }).addTo(map);
    
    // Evento para actualizar coordenadas al hacer clic en el mapa
    map.on('click', function(e) {
        updateMarkerPosition(e.latlng);
        actualizarFormularioDesdeCoords(e.latlng);
    });
    
    // Evento para actualizar coordenadas al arrastrar el marcador
    marker.on('dragend', function(e) {
        const newPos = e.target.getLatLng();
        updateMarkerPosition(newPos);
        actualizarFormularioDesdeCoords(newPos);
    });
    
    // Establecer coordenadas iniciales en los campos ocultos
    document.getElementById('latitud').value = initialCoords[0];
    document.getElementById('longitud').value = initialCoords[1];
}

// Actualizar posición del marcador y campos ocultos
function updateMarkerPosition(latlng) {
    marker.setLatLng(latlng);
    document.getElementById('latitud').value = latlng.lat;
    document.getElementById('longitud').value = latlng.lng;
    
    // Opcional: Hacer zoom más cercano al seleccionar ubicación
    if (map.getZoom() < 16) {
        map.setZoom(16);
    }
}

// Función para actualizar el formulario cuando se mueve el marcador
function actualizarFormularioDesdeCoords(latlng) {
    document.getElementById('latitud').value = latlng.lat;
    document.getElementById('longitud').value = latlng.lng;
    
    // Usar Nominatim para obtener la dirección inversa
    fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latlng.lat}&lon=${latlng.lng}`)
        .then(res => res.json())
        .then(data => {
            if (data.address) {
                actualizarCamposDesdeDireccion(data.address);
            }
        })
        .catch(error => {
            console.error('Error al obtener dirección inversa:', error);
        });
}

// Función para actualizar campos del formulario con datos de dirección
function actualizarCamposDesdeDireccion(address) {
    const cpInput = document.getElementById('codigo_postal');
    const calleInput = document.getElementById('calle');
    
    // Actualizar código postal si está disponible y no está ya lleno
    if (address.postcode && cpInput && (!cpInput.value || cpInput.value.length !== 5)) {
        cpInput.value = address.postcode;
        buscarCodigoPostal(address.postcode);
    }
    
    // Actualizar calle si está disponible y no está ya llena
    if (calleInput && !calleInput.value && address.road) {
        calleInput.value = address.road;
    }
}

// Función para manejar la búsqueda de código postal
async function buscarCodigoPostal(cp) {
    if (cp.length !== 5 || !/^\d{5}$/.test(cp)) {
        return;
    }

    const loadingElement = document.getElementById('cp-loading');
    const municipioInput = document.getElementById('municipio');
    const coloniaSelect = document.getElementById('colonia');

    // Mostrar loading
    if (loadingElement) loadingElement.classList.remove('hidden');

    if (cpCache[cp]) {
        llenarDatos(cpCache[cp]);
        if (loadingElement) loadingElement.classList.add('hidden');
        return;
    }

    try {
        const response = await fetch(`https://sepomex.icalialabs.com/api/v1/zip_codes?zip_code=${cp}`);
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        const data = await response.json();

        const zipCodes = data.zip_codes;
        cpCache[cp] = zipCodes;

        llenarDatos(zipCodes);

        if (zipCodes[0]?.d_cp) {
            actualizarMapaDesdeCP(zipCodes[0].d_cp);
        }

    } catch (error) {
        console.error('Error al buscar código postal:', error);
        mostrarError('No se pudo obtener la información del código postal');
    } finally {
        if (loadingElement) loadingElement.classList.add('hidden');
    }

    function llenarDatos(datos) {
        if (!datos?.length) {
            mostrarError('No se encontraron datos para este código postal');
            return;
        }

        municipioInput.value = datos[0].d_mnpio || '';

        coloniaSelect.innerHTML = '';
        if (datos.length === 1) {
            agregarOpcionColonia(datos[0]);
        } else {
            coloniaSelect.appendChild(crearOptionDefault());
            datos.sort((a, b) => a.d_asenta.localeCompare(b.d_asenta))
                .forEach(agregarOpcionColonia);
        }
        coloniaSelect.disabled = false;
    }

    function agregarOpcionColonia(item) {
        const option = document.createElement('option');
        option.value = item.d_asenta;
        option.textContent = `${item.d_asenta} (${item.d_tipo_asenta})`;
        coloniaSelect.appendChild(option);
    }

    function crearOptionDefault() {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = '-- Selecciona una colonia --';
        option.selected = true;
        return option;
    }

    function mostrarError(mensaje) {
        // Puedes personalizar este mensaje visualmente
        alert(mensaje);
    }

    function actualizarMapaDesdeCP(cp) {
        fetch(`https://nominatim.openstreetmap.org/search?postalcode=${cp}&country=Mexico&format=json`)
            .then(res => res.json())
            .then(data => {
                if (data[0]) {
                    const { lat, lon } = data[0];
                    if (map && marker) {
                        map.setView([lat, lon], 16);
                        marker.setLatLng([lat, lon]);
                        updateMarkerPosition({lat, lng: lon});
                    }
                }
            });
    }
}

// Función para toggle entre tipos de registro (se mantiene igual)
function toggleRegisterType(type) {
    currentFormType = type;
    
    const personTab = document.getElementById('person-tab');
    const institutionTab = document.getElementById('institution-tab');
    const personForm = document.getElementById('person-form');
    const institutionForm = document.getElementById('institution-form');
    
    personTab.classList.remove('active');
    personTab.classList.add('inactive');
    institutionTab.classList.remove('active');
    institutionTab.classList.add('inactive');
    
    personForm.classList.add('hidden');
    institutionForm.classList.add('hidden');
    
    if (type === 'person') {
        personTab.classList.remove('inactive');
        personTab.classList.add('active');
        personForm.classList.remove('hidden');
    } else if (type === 'institution') {
        institutionTab.classList.remove('inactive');
        institutionTab.classList.add('active');
        institutionForm.classList.remove('hidden');
    }
    
    if (map) {
        setTimeout(() => {
            map.invalidateSize();
        }, 350);
    }
}

// Eventos del DOM
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el mapa
    initMap();
    
    // Evento para el código postal
    const cpInput = document.getElementById('codigo_postal');
    if (cpInput) {
        cpInput.addEventListener('input', function() {
            buscarCodigoPostal(this.value);
        });
    }
    
    // Eventos para el toggle
    document.getElementById('person-tab').addEventListener('click', function() {
        toggleRegisterType('person');
    });
    
    document.getElementById('institution-tab').addEventListener('click', function() {
        toggleRegisterType('institution');
    });
});