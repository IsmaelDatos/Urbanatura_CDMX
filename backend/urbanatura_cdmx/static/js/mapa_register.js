/* =========  VARIABLES GLOBALES  ========= */
let currentFormType   = "person";   // "person" | "institution"
let personMap         = null;
let institutionMap    = null;
let personMarker      = null;
let institutionMarker = null;
const cpCache         = {};

/* =========  HELPERS  ========= */
function getActiveMap()    { return currentFormType === "person" ? personMap    : institutionMap; }
function getActiveMarker() { return currentFormType === "person" ? personMarker : institutionMarker; }

/* =========  INICIALIZAR MAPA  ========= */
function initMap(type = "person") {
  const mapId        = type === "person" ? "map-person" : "map-institution";
  const initialCoords = [19.4326, -99.1332];
  if ((type === "person" && personMap) || (type === "institution" && institutionMap)) return;
  const map = L.map(mapId).setView(initialCoords, 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
  const marker = L.marker(initialCoords, { draggable: true, autoPan: true }).addTo(map);
  if (type === "person") {
    personMap    = map;
    personMarker = marker;
  } else {
    institutionMap    = map;
    institutionMarker = marker;
  }
  map.on("click",   (e) => { updateMarkerPosition(e.latlng, type);   actualizarFormularioDesdeCoords(e.latlng); });
  marker.on("dragend", (e) => { const p = e.target.getLatLng(); updateMarkerPosition(p, type); actualizarFormularioDesdeCoords(p); });
  updateMarkerPosition({ lat: initialCoords[0], lng: initialCoords[1] }, type);
}

/* =========  ACTUALIZAR MARCADOR & INPUTS  ========= */
function updateMarkerPosition(latlng, type) {
  const mk = type === "person" ? personMarker : institutionMarker;
  if (mk) mk.setLatLng(latlng);
  const prefix = type === "person" ? "person" : "institution";
  document.getElementById(`${prefix}-latitud`).value = latlng.lat.toFixed(8);
  document.getElementById(`${prefix}-longitud`).value = latlng.lng.toFixed(8);
}

/* =========  REVERSE GEOCODING  ========= */
function actualizarFormularioDesdeCoords(latlng) {
  fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latlng.lat}&lon=${latlng.lng}`)
    .then(r => r.json())
    .then(data => { 
      if (data.address) {
        actualizarCamposDesdeDireccion(data.address, currentFormType);
      }
    })
    .catch(err => console.error("Error reverse geocoding:", err));
}
function actualizarCamposDesdeDireccion(address, formType) {
  const formPrefix = formType === "person" ? "person" : "institution";
  const cpInput = document.getElementById(`${formPrefix}-codigo_postal`);
  const calleInput = document.getElementById(`${formPrefix}-calle`);

  if (address.postcode && cpInput && (!cpInput.value || cpInput.value.length !== 5)) {
    cpInput.value = address.postcode;
    buscarCodigoPostal(address.postcode, formType);
  }
  if (calleInput && !calleInput.value && address.road) {
    calleInput.value = address.road;
  }
}

/* =========  BÚSQUEDA DE CÓDIGO POSTAL  ========= */
async function buscarCodigoPostal(cp, formType) {
  if (!/^\d{5}$/.test(cp)) return;
  
  const formPrefix = formType === "person" ? "person" : "institution";
  const loadingEl = document.getElementById(`${formPrefix}-cp-loading`);
  const municipioIn = document.getElementById(`${formPrefix}-municipio`);
  const coloniaSel = document.getElementById(`${formPrefix}-colonia`);

  if (loadingEl) loadingEl.classList.remove("hidden");
  if (cpCache[cp]) {
    llenarDatos(cpCache[cp]);
    if (loadingEl) loadingEl.classList.add("hidden");
    return;
  }
  try {
    const resp = await fetch(`https://sepomex.icalialabs.com/api/v1/zip_codes?zip_code=${cp}`);
    if (!resp.ok) throw new Error(resp.statusText);
    const data = await resp.json();
    cpCache[cp] = data.zip_codes;
    llenarDatos(cpCache[cp]);
    if (data.zip_codes[0]?.d_cp) actualizarMapaDesdeCP(data.zip_codes[0].d_cp);
  } catch (err) {
    console.error("CP fetch error:", err);
    alert("No se pudo obtener la información del código postal");
  } finally {
    if (loadingEl) loadingEl.classList.add("hidden");
  }
  function llenarDatos(arr) {
    if (!arr.length) return alert("No se encontraron datos para este código postal");
    municipioIn.value = arr[0].d_mnpio || "";
    coloniaSel.innerHTML = "";
    if (arr.length === 1) agregarOpcion(arr[0]);
    else {
      coloniaSel.appendChild(crearOptionDefault());
      arr.sort((a,b) => a.d_asenta.localeCompare(b.d_asenta)).forEach(agregarOpcion);
    }
    coloniaSel.disabled = false;
  }
  function agregarOpcion(item) {
    const opt = document.createElement("option");
    opt.value = item.d_asenta;
    opt.textContent = `${item.d_asenta} (${item.d_tipo_asenta})`;
    coloniaSel.appendChild(opt);
  }
  function crearOptionDefault() {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = "-- Selecciona una colonia --";
    opt.selected = true;
    return opt;
  }
  function actualizarMapaDesdeCP(cpVal) {
    fetch(`https://nominatim.openstreetmap.org/search?postalcode=${cpVal}&country=Mexico&format=json`)
      .then(r => r.json())
      .then(d => {
        if (!d[0]) return;
        const { lat, lon } = d[0];
        const actMap    = getActiveMap();
        const actMarker = getActiveMarker();
        if (actMap && actMarker) {
          actMap.setView([lat, lon], 16);
          actMarker.setLatLng([lat, lon]);
          updateMarkerPosition({ lat: parseFloat(lat), lng: parseFloat(lon) }, currentFormType);
        }
      });
  }
}

/* =========  TOGGLE ENTRE FORMULARIOS  ========= */
function toggleRegisterType(type) {
  currentFormType = type;

  const personTab  = document.getElementById("person-tab");
  const instTab    = document.getElementById("institution-tab");
  const personForm = document.getElementById("person-form");
  const instForm   = document.getElementById("institution-form");

  if (type === "person") {
    personTab.classList.add("active");       instTab.classList.remove("active");
    personForm.classList.remove("hidden");   instForm.classList.add("hidden");
    setTimeout(() => {
      if (!personMap) initMap("person");
      else personMap.invalidateSize();
    }, 50);
  } else {
    personTab.classList.remove("active");    instTab.classList.add("active");
    personForm.classList.add("hidden");      instForm.classList.remove("hidden");
    setTimeout(() => {
      if (!institutionMap) initMap("institution");
      else institutionMap.invalidateSize();
    }, 50);
  }
}

/* =========  EVENTOS DOM (ÚNICO LISTENER) ========= */
document.addEventListener("DOMContentLoaded", () => {
  initMap("person");
  const cpInput = document.getElementById("codigo_postal");
  if (cpInput) cpInput.addEventListener("input", () => buscarCodigoPostal(cpInput.value));
  document.getElementById("person-tab")     .addEventListener("click", () => toggleRegisterType("person"));
  document.getElementById("institution-tab").addEventListener("click", () => toggleRegisterType("institution"));
});
