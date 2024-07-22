$(document).ready(function () {
    console.log("Document ready, attempting to load histogram...");
    var scripts = document.getElementById('Histogram_Graph');
    var histogram_scores = scripts.getAttribute('histogram_scores');

    // Ensure histogram_scores is parsed as JSON
    histogram_scores = JSON.parse(histogram_scores.replace(/'/g, '"'));

    // Check if the element exists before trying to get its context
    var canvas = document.getElementById("histogramOutput");
    if (!canvas) {
        console.error("Canvas element with ID 'HistogramOutput' not found.");
        return; // Exit the function if canvas is not found
    }

    Histogram_Graph(histogram_scores);
});

function downloadHisto() {

    var downloadLink = document.querySelector('a[download="histogram_plot.png"]');
    var canvas = document.getElementById('HistogramOutput');
    downloadLink.href = HistogramChart.toDataURL('image/png');
}

function Histogram_Graph(histogram_scores) {
    var ctx = document.getElementById("histogramOutput").getContext('2d');
    var HistogramChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({ length: 256 }, (_, i) => i),
            datasets: [
                {
                    label: 'Red',
                    data: histogram_scores.red,
                    backgroundColor: 'rgb(211,6,52)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Green',
                    data: histogram_scores.green,
                    backgroundColor: 'rgba(28,129,6,0.91)',
                    borderColor: 'rgb(5,99,11)',
                    borderWidth: 2
                },
                {
                    label: 'Blue',
                    data: histogram_scores.blue,
                    backgroundColor: 'rgba(9,90,143,0.97)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    console.log("Histogram Graph loaded");
}

