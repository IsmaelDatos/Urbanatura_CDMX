document.addEventListener('DOMContentLoaded', () => {

    const map = L.map('map').setView([19.4326, -99.1332], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    const marker = L.marker([19.4326, -99.1332], { draggable: true, autoPan: true }).addTo(map);

    const cpInput        = document.getElementById('codigo_postal');
    const ciudadInput    = document.getElementById('ciudad');
    const alcaldiaInput  = document.getElementById('alcaldia');
    const coloniaSelect  = document.getElementById('colonia');
    const calleInput     = document.getElementById('calle');
    const latInput       = document.getElementById('latitud');
    const lngInput       = document.getElementById('longitud');
    const loadingIndicator = document.getElementById('cp-loading');

    const cpCache = {};
    cpInput.addEventListener('input', () => {
        clearErrorMessages();
        const cp = cpInput.value.trim();
        if (cp.length === 5 && /^\d+$/.test(cp)) buscarCodigoPostal(cp);
    });
    marker.on('dragend', e => actualizarFormularioDesdeCoords(e.target.getLatLng()));
    map.on('click',   e => { marker.setLatLng(e.latlng); actualizarFormularioDesdeCoords(e.latlng); });
    latInput.addEventListener('input', manejarCoordenadasManual);
    lngInput.addEventListener('input', manejarCoordenadasManual);

    let coordTimer = null;
    function manejarCoordenadasManual () {
        clearTimeout(coordTimer);
        coordTimer = setTimeout(() => {
            const lat = parseFloat(latInput.value.replace(',', '.'));
            const lng = parseFloat(lngInput.value.replace(',', '.'));

            const latOk = isFinite(lat) && lat >= -90  && lat <=  90;
            const lngOk = isFinite(lng) && lng >= -180 && lng <= 180;
            if (!latOk || !lngOk) return;

            map.setView([lat, lng], 16);
            marker.setLatLng([lat, lng]);
            actualizarFormularioDesdeCoords({ lat, lng });
        }, 400);
    }
    async function buscarCodigoPostal(cp) {
        if (cpCache[cp]) return llenarDatos(cpCache[cp]);
        showLoading(true); resetearCampos();
        try {
            const res   = await fetch(`https://sepomex.icalialabs.com/api/v1/zip_codes?zip_code=${cp}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data  = await res.json();
            cpCache[cp] = data.zip_codes;
            llenarDatos(data.zip_codes);
            if (data.zip_codes[0]?.d_cp) actualizarMapaDesdeCP(data.zip_codes[0].d_cp);
        } catch (err) {
            console.error(err);
            mostrarError('Error al obtener datos. Intenta nuevamente.');
        } finally {
            showLoading(false);
        }
    }
    function llenarDatos(datos) {
        if (!datos?.length) return mostrarError('No se encontraron datos para este código postal');
        if (ciudadInput)   ciudadInput.value  = datos[0].d_ciudad  || '';
        alcaldiaInput.value                  = datos[0].d_mnpio   || '';

        coloniaSelect.innerHTML = '';
        if (datos.length === 1) {
            agregarOpcionColonia(datos[0]);
        } else {
            coloniaSelect.appendChild(crearOptionDefault());
            datos.sort((a, b) => a.d_asenta.localeCompare(b.d_asenta)).forEach(agregarOpcionColonia);
        }
        coloniaSelect.disabled = false;
    }
    function actualizarMapaDesdeCP(cp) {
        fetch(`https://nominatim.openstreetmap.org/search?postalcode=${cp}&country=Mexico&format=json`)
            .then(res => res.json())
            .then(data => {
                if (!data[0]) return;
                const { lat, lon } = data[0];
                map.setView([lat, lon], 16);
                marker.setLatLng([lat, lon]);
                latInput.value = parseFloat(lat).toFixed(6);
                lngInput.value = parseFloat(lon).toFixed(6);
            });
    }
    function actualizarFormularioDesdeCoords({ lat, lng }) {
        latInput.value = lat.toFixed(6);
        lngInput.value = lng.toFixed(6);
        fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`)
            .then(r => r.json())
            .then(data => {
                const addr = data.address || {};
                if (addr.postcode && addr.postcode !== cpInput.value) {
                    cpInput.value = addr.postcode;
                    buscarCodigoPostal(addr.postcode);
                }
                if (!calleInput.value && addr.road) {
                    calleInput.value = addr.house_number ? `${addr.road} ${addr.house_number}` : addr.road;
                }
            });
    }
    function agregarOpcionColonia(item) {
        const opt = document.createElement('option');
        opt.value = item.d_asenta;
        opt.textContent = `${item.d_asenta} (${item.d_tipo_asenta})`;
        coloniaSelect.appendChild(opt);
    }
    function crearOptionDefault() {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = '-- Selecciona una colonia --';
        opt.selected = true;
        return opt;
    }
    function resetearCampos() {
        if (ciudadInput) ciudadInput.value = '';
        alcaldiaInput.value = '';
        coloniaSelect.innerHTML = '<option value="">Primero ingresa tu código postal</option>';
        coloniaSelect.disabled = true;
    }

    function showLoading(show) { loadingIndicator.classList.toggle('hidden', !show); }
    function mostrarError(msg)  { clearErrorMessages(); insertError(msg); }
    function clearErrorMessages() {
        document.querySelectorAll('.error-message').forEach(el => el.remove());
    }
    function insertError(msg)   {
        const div = document.createElement('div');
        div.className = 'error-message text-red-500 text-sm mt-1';
        div.textContent = msg;
        cpInput.parentNode.insertBefore(div, cpInput.nextSibling);
    }
});