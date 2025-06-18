document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map').setView([19.4326, -99.1332], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    const marker = L.marker([19.4326, -99.1332], {draggable: true}).addTo(map);

    const cpInput = document.getElementById('codigo_postal');
    // Si no tienes el input #ciudad, quita esta línea o crea el campo
    const ciudadInput = document.getElementById('ciudad'); 
    const alcaldiaInput = document.getElementById('alcaldia');
    const coloniaSelect = document.getElementById('colonia');
    const loadingIndicator = document.getElementById('cp-loading');
    const cpCache = {};

    cpInput.addEventListener('input', function() {
        clearErrorMessages();
        const cp = cpInput.value.trim();
        if (cp.length === 5 && /^\d+$/.test(cp)) {
            buscarCodigoPostal(cp);
        }
    });

    function buscarCodigoPostal(cp) {
        if (cpCache[cp]) {
            llenarDatos(cpCache[cp]);
            return;
        }
        showLoading(true);
        resetearCampos();
        
        fetch(`https://sepomex.icalialabs.com/api/v1/zip_codes?zip_code=${cp}`)
            .then(handleResponse)
            .then(data => {
                console.log('Datos CP:', data); // Para depurar
                cpCache[cp] = data.zip_codes;
                llenarDatos(data.zip_codes);
                if (data.zip_codes[0]?.d_cp) {
                    actualizarMapaDesdeCP(data.zip_codes[0].d_cp);
                }
            })
            .catch(handleError)
            .finally(() => showLoading(false));
    }

    function llenarDatos(datos) {
        console.log('llenarDatos:', datos); // Para depurar
        if (!datos?.length) {
            mostrarError('No se encontraron datos para este código postal');
            return;
        }

        if(ciudadInput) ciudadInput.value = datos[0].d_ciudad || '';
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

    function actualizarMapaDesdeCP(cp) {
        fetch(`https://nominatim.openstreetmap.org/search?postalcode=${cp}&country=Mexico&format=json`)
            .then(res => res.json())
            .then(data => {
                if (data[0]) {
                    const {lat, lon} = data[0];
                    map.setView([lat, lon], 15);
                    marker.setLatLng([lat, lon]);
                }
            });
    }

    marker.on('dragend', function(e) {
        actualizarFormularioDesdeCoords(e.target.getLatLng());
    });

    map.on('click', function(e) {
        marker.setLatLng(e.latlng);
        actualizarFormularioDesdeCoords(e.latlng);
    });

    function actualizarFormularioDesdeCoords(latlng) {
        document.getElementById('latitud').value = latlng.lat;
        document.getElementById('longitud').value = latlng.lng;
        
        fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latlng.lat}&lon=${latlng.lng}`)
            .then(res => res.json())
            .then(data => {
                console.log('reverse geocode:', data);
                if (data.address) {
                    actualizarCamposDesdeDireccion(data.address);
                }
            });
    }

    function actualizarCamposDesdeDireccion(address) {
        console.log('actualizarCamposDesdeDireccion:', address);
        if (address.postcode && address.postcode !== cpInput.value) {
            cpInput.value = address.postcode;
            buscarCodigoPostal(address.postcode);
        }
        
        if (!document.getElementById('calle').value && address.road) {
            let calle = address.road;
            if (address.house_number) calle += ` ${address.house_number}`;
            document.getElementById('calle').value = calle;
        }
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

    function handleResponse(response) {
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return response.json();
    }

    function handleError(error) {
        console.error('Error:', error);
        mostrarError('Error al obtener datos. Intenta nuevamente.');
    }

    function resetearCampos() {
        if(ciudadInput) ciudadInput.value = '';
        alcaldiaInput.value = '';
        coloniaSelect.innerHTML = '<option value="">Primero ingresa tu código postal</option>';
        coloniaSelect.disabled = true;
    }

    function showLoading(show) {
        loadingIndicator.classList.toggle('hidden', !show);
    }

    function mostrarError(mensaje) {
        clearErrorMessages();
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message text-red-500 text-sm mt-1';
        errorElement.textContent = mensaje;
        cpInput.parentNode.insertBefore(errorElement, cpInput.nextSibling);
    }

    function clearErrorMessages() {
        document.querySelectorAll('.error-message').forEach(el => el.remove());
    }
});
