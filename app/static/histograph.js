$(document).ready(function () {
    console.log("Document ready, attempting to load histogram...");
    var scripts = document.getElementById('Histogram_Graph');
    var histogram_scores = scripts.getAttribute('histogram_scores');

    // Ensure histogram_scores is parsed as JSON
    histogram_scores_json = JSON.parse(histogram_scores.replace(/'/g, '"'));

    // Check if the element exists before trying to get its context
    var canvas = document.getElementById("histogramOutput");
    if (!canvas) {
        console.error("Canvas element with ID 'HistogramOutput' not found.");
        return; // Exit the function if canvas is not found
    }
    Histogram_Graph(histogram_scores_json);

});

function downloadHisto() {

    // This function is used to download the histogram graph as a PNG image

    var downloadLink = document.querySelector('a[download="histogram_plot.png"]');
    var HistogramChart = document.getElementById('histogramOutput');
    downloadLink.href = HistogramChart.toDataURL('image/png');
};


function downloadHistoResults() {
    // We retrieve the histogram results
    var scripts = document.getElementById('Histogram_Graph');
    var histogram_scores = scripts.getAttribute('histogram_scores');

    // Convert histogram_scores to a proper string format
    const dataStr = JSON.stringify(JSON.parse(histogram_scores.replace(/'/g, '"')), null, 2);
    const dataUri = 'data:text/plain;charset=utf-8,' + encodeURIComponent(dataStr);

    //Those lines create a temporary link element
    const link = document.createElement('a');
    link.setAttribute('href', dataUri);
    link.setAttribute('download', 'histogram_results.txt');
    document.body.appendChild(link);

    // This line will make it so as we click the link, it will trigger the download
    link.click();

    // Remove the link element from the document
    document.body.removeChild(link);
}

function Histogram_Graph(histogram_scores) {
    // Retrieving the element histogramOutput from the HTML file
    var ctx = document.getElementById("histogramOutput").getContext('2d');

    // Creating a new histogram chart
    var HistogramChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({ length: 256 }, (_, i) => i),
            //Creating the datasets for the histogram chart
            datasets: [
                {
                    // Red color
                    label: 'Red',
                    data: histogram_scores.red,
                    backgroundColor: 'rgb(211,6,52)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2
                },
                {
                    // Green color
                    label: 'Green',
                    data: histogram_scores.green,
                    backgroundColor: 'rgba(28,129,6,0.91)',
                    borderColor: 'rgb(5,99,11)',
                    borderWidth: 2
                },
                {
                    // Blue color
                    label: 'Blue',
                    data: histogram_scores.blue,
                    backgroundColor: 'rgba(9,90,143,0.97)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                }
            ]
        },
        // Options for the histogram chart (Starts at 0 on both axes)
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
    // Check if the canvas has been correctly loaded
}

