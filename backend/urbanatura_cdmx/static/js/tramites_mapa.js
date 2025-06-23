document.addEventListener('DOMContentLoaded', function() {
    /***********************
     * Configuración Mapa *
     ***********************/
    const map = L.map('map').setView([19.4326, -99.1332], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    const marker = L.marker([19.4326, -99.1332], {
        draggable: true,
        autoPan: true
    }).addTo(map);

    /*****************************
     * Elementos del Formulario *
     *****************************/
    const cpInput = document.getElementById('codigo_postal');
    const alcaldiaInput = document.getElementById('alcaldia');
    const coloniaSelect = document.getElementById('colonia');
    const calleInput = document.getElementById('calle');
    const numExtInput = document.getElementById('num_ext');
    const numIntInput = document.getElementById('num_int');
    const latInput = document.getElementById('lat_display');  // Cambiado a lat_display
    const lngInput = document.getElementById('lng_display');  // Cambiado a lng_display
    const loadingIndicator = document.getElementById('cp-loading');
    const cpCache = {};

    /**************************
     * Event Listeners *
     **************************/
    cpInput.addEventListener('input', function() {
        const cp = cpInput.value.trim();
        if (cp.length === 5 && /^\d+$/.test(cp)) {
            buscarCodigoPostal(cp);
        }
    });

    // Coordenadas manuales
    latInput.addEventListener('change', actualizarMapaDesdeCoords);
    lngInput.addEventListener('change', actualizarMapaDesdeCoords);

    /**************************
     * Funciones del Mapa *
     **************************/
    function actualizarMapaDesdeCoords() {
        const lat = parseFloat(latInput.value);
        const lng = parseFloat(lngInput.value);
        
        if (!isNaN(lat) && !isNaN(lng)) {
            map.setView([lat, lng], 16);
            marker.setLatLng([lat, lng]);
        }
    }

    marker.on('dragend', function(e) {
        const {lat, lng} = e.target.getLatLng();
        latInput.value = lat.toFixed(6);
        lngInput.value = lng.toFixed(6);
        actualizarFormularioDesdeCoords(e.target.getLatLng());
    });

    map.on('click', function(e) {
        marker.setLatLng(e.latlng);
        latInput.value = e.latlng.lat.toFixed(6);
        lngInput.value = e.latlng.lng.toFixed(6);
        actualizarFormularioDesdeCoords(e.latlng);
    });

    /**************************
     * Funciones SEPOMEX *
     **************************/
    async function buscarCodigoPostal(cp) {
        if (cpCache[cp]) {
            llenarDatos(cpCache[cp]);
            return;
        }

        showLoading(true);
        
        try {
            const response = await fetch(`https://sepomex.icalialabs.com/api/v1/zip_codes?zip_code=${cp}`);
            const data = await response.json();
            
            cpCache[cp] = data.zip_codes;
            llenarDatos(data.zip_codes);
            
            if (data.zip_codes[0]?.d_cp) {
                actualizarMapaDesdeCP(data.zip_codes[0].d_cp);
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarError('Error al obtener datos. Intenta nuevamente.');
        } finally {
            showLoading(false);
        }
    }

    function llenarDatos(datos) {
        if (!datos?.length) {
            mostrarError('No se encontraron datos para este código postal');
            return;
        }

        alcaldiaInput.value = datos[0].d_mnpio || '';
        
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

    /**************************
     * Funciones Auxiliares *
     **************************/
    function actualizarFormularioDesdeCoords(latlng) {
        fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latlng.lat}&lon=${latlng.lng}`)
            .then(res => res.json())
            .then(data => {
                if (data.address) {
                    if (!cpInput.value && data.address.postcode) {
                        cpInput.value = data.address.postcode;
                        buscarCodigoPostal(data.address.postcode);
                    }
                    if (!calleInput.value && data.address.road) {
                        calleInput.value = data.address.road;
                    }
                }
            });
    }

    function actualizarMapaDesdeCP(cp) {
        fetch(`https://nominatim.openstreetmap.org/search?postalcode=${cp}&country=Mexico&format=json`)
            .then(res => res.json())
            .then(data => {
                if (data[0]) {
                    const {lat, lon} = data[0];
                    map.setView([lat, lon], 16);
                    marker.setLatLng([lat, lon]);
                    latInput.value = lat.toFixed(6);
                    lngInput.value = lon.toFixed(6);
                }
            });
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

    function showLoading(show) {
        loadingIndicator.classList.toggle('hidden', !show);
    }

    function mostrarError(mensaje) {
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message text-red-500 text-sm mt-1';
        errorElement.textContent = mensaje;
        cpInput.parentNode.insertBefore(errorElement, cpInput.nextSibling);
    }
});
