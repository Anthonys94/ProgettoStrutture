var Url = 'http://127.0.0.1:5002';
var globalVariableStrutture;
var globalVariableProva;
var globalVariableMateriale;

function successStrutture(result) {
    globalVariableStrutture = result;
    // aggiungi le strutture
    var lung = globalVariableStrutture.length;
    var select = document.getElementById("ListaStrutture");
    for (step = 0; step < lung; step++) {
        var option = document.createElement("option");
        option.value = globalVariableStrutture[step]["tipologiaStruttura"];
        option.text = globalVariableStrutture[step]["tipologiaStruttura"];
        select.appendChild(option);
    }
}

function successMateriale(result) {
    globalVariableMateriale = result;
    // aggiungi i materiali
    var lung = globalVariableMateriale.length;
    var select = document.getElementById("ListaMateriali");
    for (step = 0; step < lung; step++) {
        var option = document.createElement("option");
        option.value = globalVariableMateriale[step]["materiale"];
        option.text = globalVariableMateriale[step]["materiale"];
        select.appendChild(option);
    }
}

function successProva(result) {
    globalVariableProva = result;
    // aggiungi le prove
    var lung = globalVariableProva.length;
    var select = document.getElementById("ListaProve");
    for (step = 0; step < lung; step++) {
        var option = document.createElement("option");
        option.value = globalVariableProva[step]["tipoProva"];
        option.text = globalVariableProva[step]["tipoProva"];
        select.appendChild(option);
    }
}

function successGetProvince(result) {
    var lung = result.length;
    var select = document.getElementById("ListaProvince");
    for (step = 0; step < lung; step++) {
        var option = document.createElement("option");
        option.value = result[step]["provincia"];
        option.text = result[step]["provincia"];
        select.appendChild(option);
    }
}

function successQuerybyPratica(result) {
    if (result.length == 0) {
        alert('Pratica non trovata')
    } else {
        document.getElementById('RicercaNumeroPratica').hidden = true;
        document.getElementById('Annulla').hidden = true;
        console.log(result);
        var table = document.getElementById("TableRis");
        createTable(table, result);
        document.getElementById("SezTableR").hidden = false;
    }

}

function successQuerybyCampo(result) {
    document.getElementById('RicercaperCampi').hidden = true;
    document.getElementById('Annulla').hidden = true;
    console.log(result);
    var table = document.getElementById("TableRis");
    createTable(table, result);
    document.getElementById("SezTableR").hidden = false;
}

function createTable(table, result) {
    var lun = result.length;
    for (var index = 0; index < lun; index++) {
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var third = row.insertCell(2);
        var four = row.insertCell(3);
        var five = row.insertCell(4);
        var six = row.insertCell(5);
        var seven = row.insertCell(6);
        var eight = row.insertCell(7);
        var nine = row.insertCell(8);
        var ten = row.insertCell(9);

        fistCell.append(document.createTextNode(result[index]['Rif']));
        secondCell.append(document.createTextNode(result[index]['Tipologia']))
        third.append(document.createTextNode(result[index]['Committente']));
        four.append(document.createTextNode(result[index]['data']));
        five.append(document.createTextNode(result[index]['provincia']));
        six.append(document.createTextNode(result[index]['comune']));
        seven.append(document.createTextNode(result[index]['struttura']));
        eight.append(document.createTextNode(result[index]['materiale']));
        nine.append(document.createTextNode(result[index]['prova']));
        var btn = document.createElement('input');
        btn.id = "btn_" + String(index);
        btn.type = "button";
        btn.value = "download";
        var tupla = result[index];
        /*btn.addEventListener('click', function (){
            DownloadFc();
        },false);*/
        btn.onclick = (function (tupla) {
            return function () {
                DownloadFc(tupla)
            };
        })(tupla);


        ten.append(btn)
    }
}

function DownloadFc(x) {
    var file;
    if (x['Tipologia']=="certificato"){
        var app = x['Rif'].split('/')
        if (app.length == 1){
            file = app[0] + "_unique.pdf";
        }else {
            file = app[0] + "_" +app[1] + ".pdf";
        }
    }else if (x['Tipologia']=="apertura pratica"){
        file = x['Rif'].split('/')[0] + "_apertura.pdf";
    }else if (x['Tipologia']=="foglio di lavoro"){
        file = x['Rif'].split('/')[0] + "_foglio_lavoro.pdf"
    }
    $.ajax({
        url: Url + "/download",
        type: "GET",
        data: {
            file:file,
        },
        xhrFields: {
                responseType: 'blob'
        },
        success: function (response, status, xhr) {

            // check for a filename
            var filename = "";
            var disposition = xhr.getResponseHeader('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
            }

            var type = xhr.getResponseHeader('Content-Type');
            var blob = new Blob([response], {type: type});

            if (typeof window.navigator.msSaveBlob !== 'undefined') {
                // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                window.navigator.msSaveBlob(blob, filename);
            }else{
                var URL = window.URL || window.webkitURL;
                var downloadUrl = URL.createObjectURL(blob);

                if (filename) {
                    // use HTML5 a[download] attribute to specify filename
                    var a = document.createElement("a");
                    // safari doesn't support this yet
                    if (typeof a.download === 'undefined') {
                        window.location = downloadUrl;
                    } else {
                        a.href = downloadUrl;
                        a.download = filename;
                        document.body.appendChild(a);
                        a.click();
                    }
                } else {
                    window.location = downloadUrl;
                }

                setTimeout(function () {
                    URL.revokeObjectURL(downloadUrl);
                }, 100); // cleanup
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });

}

function deleteTable(table) {

    righe = table.getElementsByTagName("tr");
    l = righe.length;
    for (i = 1; i < l; i++) {
        table.deleteRow(1);
    }

}

$("#ListaProvince").change(function () {
    console.log(document.getElementById("ListaProvince").value);
    // chiamare i comuni
    var select = document.getElementById("ListaComuni");
    select.options.length = 0;
    var option = document.createElement("option");
    option.value = "";
    option.text = "Scegli Comune";
    option.selected = true;
    select.appendChild(option);
    if (document.getElementById("ListaProvince").value != "") {
        $.ajax({
            url: Url + "/getComuni",
            type: "get", //send it through get method
            data: {
                provincia: document.getElementById("ListaProvince").value
            },
            success: function (response) {
                var lung = response.length;
                var select = document.getElementById("ListaComuni");
                for (step = 0; step < lung; step++) {
                    var option = document.createElement("option");
                    option.value = response[step]["comune"];
                    option.text = response[step]["comune"];
                    select.appendChild(option);
                }
            },
            error: function (xhr) {
                console.log("Error ${xhr}");
            }
        });

    }

});

$("#and").change(function () {
    document.getElementById("or").checked = false;
});

$("#or").change(function () {
    document.getElementById("and").checked = false;
});

$('.input100').each(function () {
    $(this).on('blur', function () {
        if ($(this).val().trim() != "") {
            $(this).addClass('has-val');
        } else {
            $(this).removeClass('has-val');
        }
    })
});

$('#bntNewRicercaPratica').on('click', function () {
    var table = document.getElementById("TableRis");
    deleteTable(table);
    document.getElementById('RicercaNumeroPratica').hidden = false;
    document.getElementById('RicercaperCampi').hidden = true;
    document.getElementById('Annulla').hidden = false;
    document.getElementById("DivResult").hidden = true;
    document.getElementById("SezTableR").hidden = true;

});

$('#bntNewRicercaCampo').on('click', function () {
    var table = document.getElementById("TableRis");
    deleteTable(table);
    document.getElementById('RicercaNumeroPratica').hidden = true;
    document.getElementById('RicercaperCampi').hidden = false;
    document.getElementById('Annulla').hidden = false;
    document.getElementById("DivResult").hidden = true;
    document.getElementById("SezTableR").hidden = true;


});

$('#Annulla').on('click', function () {
    var table = document.getElementById("TableRis");
    deleteTable(table);
    document.getElementById('RicercaNumeroPratica').hidden = true;
    document.getElementById('RicercaperCampi').hidden = true;
    document.getElementById('Annulla').hidden = true;
    document.getElementById("DivResult").hidden = true;
    document.getElementById("SezTableR").hidden = true;
});

$('#RicercaPratica').on('click', function () {
    if (document.getElementById('nPratica').value == "") {
        alert('Inserire un numero di pratica');
    } else {
        $.ajax({
            type: 'GET',
            url: Url + '/DoquerybyPratica',
            data: {
                NumeroPratica: document.getElementById('nPratica').value
            },
            success: successQuerybyPratica,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    }

});

$('#RicercaCampi').on('click', function () {
    if (document.getElementById('DataStart').value == "" &&
        document.getElementById('DataEnd').value == "" &&
        document.getElementById('ListaProvince').value == "" &&
        document.getElementById('ListaComuni').value == "" &&
        document.getElementById('idAltroLuogo').value == "" &&
        document.getElementById('idCommittente').value == "" &&
        document.getElementById('iddesc').value == "" &&
        document.getElementById('ListaMateriali').value == "" &&
        document.getElementById('ListaStrutture').value == "" &&
        document.getElementById('ListaProve').value == "") {
        alert('Inserire almeno un campo')
    } else {
        DataStart = new Date(document.getElementById('DataStart').value);
        DataEnd = new Date(document.getElementById('DataEnd').value);
        if (DataEnd.getTime() < DataStart.getTime()) {
            alert('Intervallo temporale non corretto');
        } else {
            if (document.getElementById("or").checked) {
                var criterio = "or"
            } else {
                var criterio = 'and'
            }
            $.ajax({
                type: 'GET',
                url: Url + '/DoquerybyCampi',
                data: {
                    DataStart: document.getElementById('DataStart').value,
                    DataEnd: document.getElementById('DataEnd').value,
                    Provincia: document.getElementById('ListaProvince').value,
                    Comune: document.getElementById('ListaComuni').value,
                    AltroLuogo: document.getElementById('idAltroLuogo').value,
                    Committente: document.getElementById('idCommittente').value,
                    Descrizione: document.getElementById('iddesc').value,
                    Materiale: document.getElementById('ListaMateriali').value,
                    Struttura: document.getElementById('ListaStrutture').value,
                    Prova: document.getElementById('ListaProve').value,
                    criterio: criterio
                },
                success: successQuerybyCampo,
                error: function (error) {
                    console.log("Error ${error}");
                }
            });
        }
    }

});
/*
$('#btnUpload').on('click', function () {
    if (document.getElementById('DataStart').value == "" && document.getElementById('DataEnd').value ==""){
        alert('Specificare un intervallo temporale')
    }
    else{
        DataStart = new Date(document.getElementById('DataStart').value);
        DataEnd = new Date(document.getElementById('DataEnd').value);
        if (DataEnd.getTime() < DataStart.getTime()){
            alert('Intervallo temporale non corretto');
        }else{
            if (document.getElementById("or").checked){
                var criterio = "or"
            }else{
                var criterio= 'and'
            }
            $.ajax({
                type: 'GET',
                url:  Url+ '/Doquery',
                data: {
                    DataStart: document.getElementById('DataStart').value,
                    DataEnd: document.getElementById('DataEnd').value,
                    Provincia: document.getElementById("ListaProvince").value,
                    Comune: document.getElementById("ListaComuni").value,
                    Criterio: criterio
                },
                success: successQuery,
                error: function(error){
                    console.log("Error ${error}");
        }
    });
        }
    }

});
*/

$(document).ready(function () {
    var cookie = {};
    //cookie= JSON.parse(cookie);

    elementC = document.cookie.split("; ")

    for (index = 0; index < elementC.length; index++) {
        app = elementC[index].split("=");
        cookie[app[0]] = app[1];
    }
    document.getElementById('welcome').value = "Benvenuto: " + cookie['username'];

    $.ajax({
        url: Url + "/getStrutture",
        type: "GET",
        success: successStrutture,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url + "/getProva",
        type: "GET",
        success: successProva,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url + "/getMateriale",
        type: "GET",
        success: successMateriale,
        error: function (error) {
            console.log("Error ${error}");
        }
    });


    //province
    $.ajax({
        url: Url + "/getProvince",
        type: "GET",
        success: successGetProvince,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

});
