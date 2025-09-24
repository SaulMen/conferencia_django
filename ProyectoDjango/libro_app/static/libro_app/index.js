let currentXML = '';
        
function loadXMLFile(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('xmlContent').value = e.target.result;
            currentXML = e.target.result;
        };
        reader.readAsText(file);
    }
}

async function validateXML() {
    const xmlContent = document.getElementById('xmlContent').value;
    if (!xmlContent.trim()) {
        showError('Por favor, cargue un archivo XML o pegue el contenido.');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/validate_xml/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `xml_content=${encodeURIComponent(xmlContent)}`
        });

        const data = await response.json();
        showLoading(false);

        if (data.success) {
            displayConsoleOutput('Validación XML exitosa:', {
                message: data.message,
                preview: data.preview_stats,
                architecture: 'Validación realizada en Django (MVT Pattern)'
            });
            currentXML = xmlContent;
        } else {
            showError('Validación fallida: ' + data.error);
        }
    } catch (error) {
        showLoading(false);
        showError('Error de validación: ' + error.message);
    }
}

async function processXML() {
    const xmlContent = document.getElementById('xmlContent').value;
    if (!xmlContent.trim()) {
        showError('Por favor, cargue un archivo XML o pegue el contenido.');
        return;
    }

    showLoading(true);
    currentXML = xmlContent;

    try {
        const response = await fetch('/upload_xml/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `xml_content=${encodeURIComponent(xmlContent)}`
        });

        const data = await response.json();
        showLoading(false);

        if (data.success) {
            displayConsoleOutput('Procesamiento completo:', {
                django_validation: data.django_validation,
                flask_processing: data.flask_processing,
                architecture_note: data.architecture_note
            });
        } else {
            showError('Error: ' + data.error);
        }
    } catch (error) {
        showLoading(false);
        showError('Error de conexión: ' + error.message);
    }
}

async function analyzeByGenre() {
    if (!currentXML) {
        showError('Primero debe cargar un archivo XML.');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/books_by_genre/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `xml_content=${encodeURIComponent(currentXML)}`
        });

        const data = await response.json();
        showLoading(false);

        if (data.success && data.data.genres) {
            displayConsoleOutput('Análisis por género:', {
                source: data.source,
                data: data.data
            });
            createGenreChart(data.data.genres);
        } else {
            showError('Error al analizar géneros: ' + (data.error || 'Error desconocido'));
        }
    } catch (error) {
        showLoading(false);
        showError('Error: ' + error.message);
    }
}

async function analyzePrices() {
    if (!currentXML) {
        showError('Primero debe cargar un archivo XML.');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/price_analysis/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `xml_content=${encodeURIComponent(currentXML)}`
        });

        const data = await response.json();
        showLoading(false);

        if (data.success && data.data.price_stats) {
            displayConsoleOutput('Análisis de precios:', {
                source: data.source,
                data: data.data
            });
            createPriceChart(data.data.price_ranges);
        } else {
            showError('Error al analizar precios: ' + (data.error || 'Error desconocido'));
        }
    } catch (error) {
        showLoading(false);
        showError('Error: ' + error.message);
    }
}

async function publicationTimeline() {
    if (!currentXML) {
        showError('Primero debe cargar un archivo XML.');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/publication_timeline/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `xml_content=${encodeURIComponent(currentXML)}`
        });

        const data = await response.json();
        showLoading(false);

        if (data.success && data.data.timeline) {
            displayConsoleOutput('📅 Timeline de publicaciones:', {
                source: data.source,
                data: data.data
            });
            createTimelineChart(data.data.timeline);
        } else {
            showError('Error al generar timeline: ' + (data.error || 'Error desconocido'));
        }
    } catch (error) {
        showLoading(false);
        showError('Error: ' + error.message);
    }
}

async function showSystemInfo() {
    try {
        const response = await fetch('/system_info/');
        const data = await response.json();
        
        displayConsoleOutput('Información del Sistema:', {
            note: 'Este sistema NO usa base de datos',
            architecture: data.architecture,
            data_flow: 'XML → Django (Validación) → Flask (ElementTree) → Django (Presentación)',
            mvt_pattern: data.mvt_pattern,
            mvc_vs_mvt: data.mvc_vs_mvt
        });
    } catch (error) {
        showError('Error al obtener información del sistema: ' + error.message);
    }
}

function createGenreChart(genres) {
    const ctx = document.getElementById('genreCanvas').getContext('2d');
    document.getElementById('genreChart').style.display = 'block';

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(genres),
            datasets: [{
                data: Object.values(genres),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                    '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createPriceChart(priceRanges) {
    const ctx = document.getElementById('priceCanvas').getContext('2d');
    document.getElementById('priceChart').style.display = 'block';

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(priceRanges),
            datasets: [{
                label: 'Cantidad de libros',
                data: Object.values(priceRanges),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createTimelineChart(timeline) {
    const ctx = document.getElementById('timelineCanvas').getContext('2d');
    document.getElementById('timelineChart').style.display = 'block';

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(timeline).sort(),
            datasets: [{
                label: 'Libros publicados',
                data: Object.keys(timeline).sort().map(year => timeline[year]),
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function displayConsoleOutput(title, data) {
    const output = document.getElementById('consoleOutput');
    const timestamp = new Date().toLocaleTimeString();
    
    output.innerHTML += `
        <div style="border-bottom: 1px solid #34495e; padding-bottom: 10px; margin-bottom: 10px;">
            <strong style="color: #3498db;">[${timestamp}] ${title}</strong><br>
            <pre style="white-space: pre-wrap; margin-top: 5px;">${JSON.stringify(data, null, 2)}</pre>
        </div>
    `;
    output.scrollTop = output.scrollHeight;
}

function showError(message) {
    const output = document.getElementById('consoleOutput');
    const timestamp = new Date().toLocaleTimeString();
    output.innerHTML += `
        <div style="color: #e74c3c; border-bottom: 1px solid #34495e; padding-bottom: 10px; margin-bottom: 10px;">
            <strong>[${timestamp}] ERROR:</strong> ${message}
        </div>
    `;
    output.scrollTop = output.scrollHeight;
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.add('show');
    } else {
        loading.classList.remove('show');
    }
}

function clearResults() {
    document.getElementById('consoleOutput').innerHTML = '';
    document.getElementById('genreChart').style.display = 'none';
    document.getElementById('priceChart').style.display = 'none';
    document.getElementById('timelineChart').style.display = 'none';
}