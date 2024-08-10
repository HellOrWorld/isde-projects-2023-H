

$(document).ready(function () {
    // This part of the code is used to get the classification scores from the HTML script tag
    // and pass it to the makeGraph function
    var scripts = document.getElementById('makeGraph');
    var classification_scores = scripts.getAttribute('classification_scores');
    makeGraph(classification_scores);
    // This part of the code is to execute the makeGraph function when the page is loaded
});


function downloadGraph() {

    // This function is used to download the classification graph as a PNG image
    var downloadLink = document.querySelector('a[download="plot.png"]');
    var canvas = document.getElementById('classificationOutput');
    downloadLink.href = canvas.toDataURL('image/png');
}

function downloadClassificationResults() {
    // We take the classification scores from the script tag
    var scripts = document.getElementById('makeGraph');
    var classification_scores = scripts.getAttribute('classification_scores');

    // Convert the classification scores to a string format
    const dataStr = JSON.stringify(JSON.parse(classification_scores), null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

    //Those lines create a temporary link element
    const link = document.createElement('a');
    link.setAttribute('href', dataUri);
    link.setAttribute('download', 'classification_scores.json');
    document.body.appendChild(link);

    // This line will make it so as we click the link, it will trigger the download
    link.click();

    // Remove the link element from the document
    document.body.removeChild(link);
}


function makeGraph(results) {
    console.log(results);
    results = JSON.parse(results);
    var ctx = document.getElementById("classificationOutput").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: [results[0][0], results[1][0], results[2][0], results[3][0], results[4][0]],
            datasets: [{
                label: 'Output scores',
                data: [results[0][1], results[1][1], results[2][1], results[3][1], results[4][1]],
                backgroundColor: [
                    'rgba(26,74,4,0.8)',
                    'rgba(117,0,20,0.8)',
                    'rgba(121,87,3,0.8)',
                    'rgba(6,33,108,0.8)',
                    'rgba(63,3,85,0.8)',
                ],
                borderColor: [
                    'rgba(26,74,4)',
                    'rgba(117,0,20)',
                    'rgba(121,87,3)',
                    'rgba(6,33,108)',
                    'rgba(63,3,85)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}