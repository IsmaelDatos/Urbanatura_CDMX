document.addEventListener('DOMContentLoaded', () => {
    const centroCDMX = [19.4326, -99.1332];

    const cartoPositron = L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        {
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> ' +
                'contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        }
    );

    const openStreetMap = L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        }
    );

    const map = L.map('mapa', {
        center: centroCDMX,
        zoom: 12,
        layers: [cartoPositron]
    });

    const arbolesLayer = L.layerGroup().addTo(map);
    const podasLayer = L.layerGroup();
    const derribosLayer = L.layerGroup();

    const baseLayers = {
        'CartoDB Positron': cartoPositron,
        'OpenStreetMap': openStreetMap
    };

    const overlayLayers = {
        'Árboles': arbolesLayer,
        'Podas': podasLayer,
        'Derribos': derribosLayer
    };

    L.control.layers(baseLayers, overlayLayers, { collapsed: false }).addTo(map);

    function getColorByCondition(condicion) {
        switch ((condicion || '').toLowerCase()) {
            case 'muy buena': return '#4CAF50';
            case 'buena': return '#8BC34A';
            case 'susceptible de mejora': return '#FFC107';
            case 'irrecuperable': return '#9E9E9E';
            default: return '#607D8B';
        }
    }

    const podaIcon = L.icon({
        iconUrl: '/static/images/poda-icon.png',
        iconSize: [25, 25],
        iconAnchor: [12, 25],
        popupAnchor: [0, -25]
    });

    const derriboIcon = L.icon({
        iconUrl: '/static/images/derribo-icon.png',
        iconSize: [25, 25],
        iconAnchor: [12, 25],
        popupAnchor: [0, -25]
    });

    async function cargarDatos() {
        try {
            const response = await fetch('/datos-mapa/');
            const data = await response.json();

            arbolesLayer.clearLayers();
            podasLayer.clearLayers();
            derribosLayer.clearLayers();

            data.arboles?.forEach(arbol => {
                const circle = L.circle([arbol.latitud, arbol.longitud], {
                    color: getColorByCondition(arbol.condicion_general),
                    fillColor: getColorByCondition(arbol.condicion_general),
                    fillOpacity: 0.7,
                    radius: arbol.diametro_tronco * 0.5  // Radio basado en diámetro
                }).bindPopup(
                    `<b>Árbol #${arbol.id}</b><br>Condición: ${arbol.condicion_general}`
                );
                arbolesLayer.addLayer(circle);
            });

            data.podas?.forEach(poda => {
                const marker = L.marker([poda.latitud, poda.longitud], { 
                    icon: podaIcon 
                }).bindPopup(`<b>Poda #${poda.id}</b>`);
                podasLayer.addLayer(marker);
            });
            data.derribos?.forEach(derribo => {
                const marker = L.marker([derribo.latitud, derribo.longitud], { 
                icon: derriboIcon 
                }).bindPopup(`<b>Derribo #${derribo.id}</b>`);
                derribosLayer.addLayer(marker);
            });

        } catch (err) {
            console.error('Error al cargar datos:', err);
        }
    }

    cargarDatos();
    setInterval(cargarDatos, 300000);

    L.marker(centroCDMX)
        .addTo(map)
        .bindPopup('Centro de la CDMX')
        .openPopup();

    window.mapa = { map, cargarDatos };
});
