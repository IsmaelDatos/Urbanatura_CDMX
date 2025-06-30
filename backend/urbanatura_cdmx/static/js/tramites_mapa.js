document.addEventListener('DOMContentLoaded', () => {
  const map = L.map('map').setView([19.4326, -99.1332], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
  }).addTo(map);
  const marker = L.marker([0, 0], { 
    draggable: true, 
    autoPan: true,
    opacity: 0 
  });
  const cpInput = document.getElementById('codigo_postal');
  const alcaldiaInput = document.getElementById('alcaldia');
  const coloniaSelect = document.getElementById('colonia');
  const calleInput = document.getElementById('calle');
  const numExtInput = document.getElementById('num_ext');
  const numIntInput = document.getElementById('num_int');
  const latInput = document.getElementById('lat_display');
  const lngInput = document.getElementById('lng_display');
  const loadingIndicator = document.getElementById('cp-loading');
  latInput.value = '';
  lngInput.value = '';
  const cpCache = {};
  map.on('click', e => {
    if (!map.hasLayer(marker)) {
      marker.setLatLng(e.latlng).addTo(map);
      marker.setOpacity(1);
      actualizarDesdeCoords(e.latlng);
    } else {
      marker.setLatLng(e.latlng);
      actualizarDesdeCoords(e.latlng);
    }
  });
  marker.on('dragend', e => actualizarDesdeCoords(e.target.getLatLng()));
  latInput.addEventListener('input', manejarCoordenadasManuales);
  lngInput.addEventListener('input', manejarCoordenadasManuales);
  cpInput.addEventListener('input', () => {
    clearErrors();
    const cp = cpInput.value.trim();
    if (cp.length === 5 && /^\d+$/.test(cp)) buscarCP(cp);
  });
  let debounceTimer;
  function manejarCoordenadasManuales() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const lat = parseFloat(latInput.value.replace(',', '.'));
      const lng = parseFloat(lngInput.value.replace(',', '.'));
      if (!validarCoordenadas(lat, lng)) return;
      if (!map.hasLayer(marker)) {
        marker.setLatLng([lat, lng]).addTo(map).setOpacity(1);
      } else {
        marker.setLatLng([lat, lng]);
      }
      map.setView([lat, lng], 16);
      actualizarDesdeCoords({ lat, lng });
    }, 800);
  }
  function validarCoordenadas(lat, lng) {
    return isFinite(lat) && lat >= -90 && lat <= 90 &&
           isFinite(lng) && lng >= -180 && lng <= 180;
  }
  async function actualizarDesdeCoords({ lat, lng }) {
    if (validarCoordenadas(lat, lng)) {
      actualizarInputsCoordenadas(lat, lng);
      
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`);
        const data = await res.json();
        const addr = data.address || {};
        
        if (addr.postcode && addr.postcode !== cpInput.value) {
          cpInput.value = addr.postcode;
          await buscarCP(addr.postcode);
        }
        
        if (!calleInput.value && addr.road) {
          calleInput.value = addr.house_number ? `${addr.road} ${addr.house_number}` : addr.road;
        }
        
        if (!numExtInput.value && addr.house_number) {
          numExtInput.value = addr.house_number;
        }
      } catch (e) {
        console.error('Error en búsqueda inversa:', e);
      }
    }
  }
  // Modificar la función actualizarInputsCoordenadas
  function actualizarInputsCoordenadas(lat, lng) {
    if (!validarCoordenadas(lat, lng)) return;
    
    const latF = parseFloat(lat).toFixed(6);
    const lngF = parseFloat(lng).toFixed(6);
    
    // Actualizar campos visibles
    document.getElementById('lat_display').value = latF;
    document.getElementById('lng_display').value = lngF;
}
  async function buscarCP(cp) {
    if (cpCache[cp]) {
      llenarDatos(cpCache[cp]);
      return;
    }
    showLoading(true);
    resetearCampos();
    try {
      const res = await fetch(`https://sepomex.icalialabs.com/api/v1/zip_codes?zip_code=${cp}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      cpCache[cp] = data.zip_codes;
      llenarDatos(data.zip_codes);
      
      if (data.zip_codes[0]?.d_cp) {
        await centrarMapaPorCP(data.zip_codes[0].d_cp);
      }
    } catch (e) {
      console.error(e);
      mostrarError('Error al obtener datos. Intenta nuevamente.');
    } finally {
      showLoading(false);
    }
  }
  async function centrarMapaPorCP(cp) {
    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/search?postalcode=${cp}&country=Mexico&format=json`);
      const data = await res.json();
      if (!data[0]) return;
      const { lat, lon } = data[0];
      map.setView([lat, lon], 16);
      if (!map.hasLayer(marker)) {
        marker.setLatLng([lat, lon]).addTo(map).setOpacity(1);
      } else {
        marker.setLatLng([lat, lon]);
      }
      
      actualizarInputsCoordenadas(lat, lon);
    } catch (e) {
      console.error('Error al centrar mapa:', e);
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
      coloniaSelect.appendChild(crearOpcionDefault());
      datos.sort((a, b) => a.d_asenta.localeCompare(b.d_asenta))
           .forEach(agregarOpcionColonia);
    }
    coloniaSelect.disabled = false;
  }

  function agregarOpcionColonia(item) {
    const opt = document.createElement('option');
    opt.value = item.d_asenta;
    opt.textContent = `${item.d_asenta} (${item.d_tipo_asenta})`;
    coloniaSelect.appendChild(opt);
  }

  function crearOpcionDefault() {
    const opt = document.createElement('option');
    opt.value = '';
    opt.textContent = '-- Selecciona una colonia --';
    opt.selected = true;
    return opt;
  }

  function resetearCampos() {
    alcaldiaInput.value = '';
    coloniaSelect.innerHTML = '<option value="">Primero ingresa tu código postal</option>';
    coloniaSelect.disabled = true;
  }

  function showLoading(show) {
    loadingIndicator.classList.toggle('hidden', !show);
  }

  function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => el.remove());
  }

  function mostrarError(msg) {
    clearErrors();
    const div = document.createElement('div');
    div.className = 'error-message text-red-500 text-sm mt-1';
    div.textContent = msg;
    cpInput.parentNode.insertBefore(div, cpInput.nextSibling);
  }
});