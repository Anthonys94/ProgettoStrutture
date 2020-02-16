var Url = 'http://127.0.0.1:5002';

/**
 * var ctx = document.getElementById('myChart').getContext('2d');
 var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
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
 */
function successYear(result) {

    var listOfLabels = [];
    var listOfCount = [];
    var len = result.length;
    for (index = 0; index < len; index++) {
        listOfLabels.push(result[index]['name']);
        listOfCount.push(result[index]['conteggio'])
    }
    var ctx = document.getElementById('myChartYear').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: listOfLabels,
            datasets: [{
                label: listOfLabels,
                data: listOfCount,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem) {
                        return tooltipItem.yLabel;
                    }
                }
            },
            title: {
                display: true,
                text: "Conteggio documenti per decennio"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    for (index = 0; index < len - 1; index++) {

        var color = "rgba(" + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + ",";

        myChart.config.data.datasets[0].backgroundColor.push(color + "0.2)");
        myChart.config.data.datasets[0].borderColor.push(color + "1)");

    }
    myChart.update();

}

function successMateriale(result) {
    var listOfLabels = [];
    var listOfCount = [];
    var len = result.length;
    for (index = 0; index < len; index++) {
        listOfLabels.push(result[index]['name']);
        listOfCount.push(result[index]['conteggio'])
    }
    var ctx = document.getElementById('myChartMateriale').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: listOfLabels,
            datasets: [{
                label: listOfLabels,
                data: listOfCount,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem) {
                        return tooltipItem.yLabel;
                    }
                }
            },
            title: {
                display: true,
                text: "Conteggio certificati per materiale"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    for (index = 0; index < len - 1; index++) {

        var color = "rgba(" + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + ",";

        myChart.config.data.datasets[0].backgroundColor.push(color + "0.2)");
        myChart.config.data.datasets[0].borderColor.push(color + "1)");

    }
    myChart.update();
}

function successStruttura(result) {
    var listOfLabels = []
    var listOfCount = []
    var len = result.length;
    for (index = 0; index < len; index++) {
        listOfLabels.push(result[index]['name']);
        listOfCount.push(result[index]['conteggio'])
    }
    var ctx = document.getElementById('myChartStruttura').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: listOfLabels,
            datasets: [{
                label: listOfLabels,
                data: listOfCount,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem) {
                        return tooltipItem.yLabel;
                    }
                }
            },
            title: {
                display: true,
                text: "Conteggio certificati per struttura"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    for (index = 0; index < len - 1; index++) {

        var color = "rgba(" + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + ",";

        myChart.config.data.datasets[0].backgroundColor.push(color + "0.2)");
        myChart.config.data.datasets[0].borderColor.push(color + "1)");

    }
    myChart.update();


}

function successProva(result) {
    var listOfLabels = [];
    var listOfCount = [];
    var data = [];
    var len = result.length;
    for (index = 0; index < len; index++) {
        listOfLabels.push(result[index]['name']);
        listOfCount.push(result[index]['conteggio'])
    }
    var ctx = document.getElementById('myChartProva').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: listOfLabels,
            datasets: [{
                label: listOfLabels,
                data: listOfCount,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem) {
                        return tooltipItem.yLabel;
                    }
                }
            },
            title: {
                display: true,
                text: "Conteggio certificati per prova"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    for (index = 0; index < len - 1; index++) {

        var color = "rgba(" + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + "," + Math.floor(Math.random() * 255) + ",";

        myChart.config.data.datasets[0].backgroundColor.push(color + "0.2)");
        myChart.config.data.datasets[0].borderColor.push(color + "1)");

    }
    myChart.update();


}

$(document).ready(function () {
    var cookie = {};
    //cookie= JSON.parse(cookie);

    elementC = document.cookie.split("; ");

    for (index = 0; index < elementC.length; index++) {
        app = elementC[index].split("=");
        cookie[app[0]] = app[1];
    }
    document.getElementById('welcome').value = "Benvenuto: " + cookie['username'];
    $.ajax({
        url: Url + "/DoquerybyAnno",
        type: "GET",
        success: successYear,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url + "/DoquerybyMateriale",
        type: "GET",
        success: successMateriale,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url + "/DoquerybyStruttura",
        type: "GET",
        success: successStruttura,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url + "/DoquerybyProve",
        type: "GET",
        success: successProva,
        error: function (error) {
            console.log("Error ${error}");
        }
    });
});
