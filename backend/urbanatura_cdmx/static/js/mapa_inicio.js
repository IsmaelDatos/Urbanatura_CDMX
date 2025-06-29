document.addEventListener('DOMContentLoaded', function() {
    // Coordenadas del centro de la CDMX (Zócalo)
    const centroCDMX = [19.4326, -99.1332];
    
    // Crear el mapa centrado en la CDMX con un zoom adecuado
    const mapa = L.map('mapa').setView(centroCDMX, 12);

    // Añadir capa de tiles de CartoDB Positron (el mismo que usa Folium por defecto)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(mapa);

    // Opcional: Añadir un marcador en el Zócalo como ejemplo
    L.marker(centroCDMX).addTo(mapa)
        .bindPopup('Centro de la CDMX')
        .openPopup();
});