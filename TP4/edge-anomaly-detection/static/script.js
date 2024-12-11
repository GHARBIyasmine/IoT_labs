const ctx = document.getElementById('vibration-plot').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Vibration Levels',
                data: [],
                borderColor: 'blue',
                fill: false
            },
            {
                label: 'Anomalies',
                data: [],
                borderColor: 'red',
                fill: false,
                pointBackgroundColor: 'red',
                pointRadius: 5
            }
        ]
    },
    options: {
        scales: {
            x: { title: { display: true, text: 'Time' } },
            y: { title: { display: true, text: 'Vibration Level' } }
        }
    }
});

function updateChart(data) {
    const timeLabel = new Date(data.timestamp * 1000).toLocaleTimeString();
    const vibration = data.vibration;
    const isAnomaly = data.is_anomaly;

    chart.data.labels.push(timeLabel);
    chart.data.datasets[0].data.push(vibration);

    if (isAnomaly) {
        chart.data.datasets[1].data.push(vibration);
    } else {
        chart.data.datasets[1].data.push(null);
    }

    if (chart.data.labels.length > 50) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }

    chart.update();
}

async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();
    updateChart(data);
}

setInterval(fetchData, 500);
