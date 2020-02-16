var Url = 'http://127.0.0.1:5002';
var typingTimer;
var doneTypingInterval = 1500; //time in ms


$('#NPratica').on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$('#NPratica').on('keydown', function () {
    clearTimeout(typingTimer);
    //annullo modifico campi documento
    document.getElementById('idModificaDocumento').hidden = true;
    //annulla
    document.getElementById('btnAnnulla').hidden = true;
    //sezioni
    document.getElementById('idSezModificaCampi').hidden = true;
});

function doneTyping() {
    if (document.getElementById('NPratica').value != "") {
        $.ajax({
            url: Url + "/check_esistenza",
            type: "GET",
            data: {
                NumeroPratica: document.getElementById('NPratica').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    document.getElementById('idModificaDocumento').hidden = false;
                    document.getElementById('btnAnnulla').hidden = false;
                } else {
                    alert('Pratica non esistente');

                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    }

}

function successotrovaDocumento(result) {
    console.log(result)
    document.getElementById('idCommittente').value = result['committente'];
    document.getElementById('idDescrizione').value = result['descrizione'];
    document.getElementById('IdNewLuogo').value = result['altroLuogo'];
    document.getElementById('DataPratica').value = result['data'];
    document.getElementById('ListaProvince').value = result['provincia'];
    var comune = result['comune'];
    console.log(document.getElementById("ListaProvince").value);
    // chiamare i comuni
    var select = document.getElementById("ListaComuni");
    select.options.length = 0;
    var option = document.createElement("option");
    option.value = "";
    option.text = "Scegli Comune";
    option.selected = true;
    option.disabled = true;
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
                select.value = comune;
            }, error: function (xhr) {
                console.log("Error ${xhr}");
            }
        });
    }

}

// bottoni alle operazioni
$('#btnAnnulla').on('click', function () {
    document.getElementById('idModificaDocumento').hidden = true;
    document.getElementById('btnAnnulla').hidden = true;
    document.getElementById('NPratica').value = "";
    document.getElementById('idSezModificaCampi').hidden = true;
});

$('#idModificaDocumento').on('click', function () {
    document.getElementById('idSezModificaCampi').hidden = false;

    if (document.getElementById('NPratica').value != "") {
        //trova il documento
        $.ajax({
            url: Url + "/trovaDocumento",
            type: "GET",
            data: {
                NumeroPratica: document.getElementById('NPratica').value
            },
            success: successotrovaDocumento,
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }
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

$("#ListaProvince").change(function () {
    console.log(document.getElementById("ListaProvince").value);
    // chiamare i comuni
    var select = document.getElementById("ListaComuni");
    select.options.length = 0;
    var option = document.createElement("option");
    option.value = "";
    option.text = "Scegli Comune";
    option.selected = true;
    option.disabled = true;
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

$(document).ready(function () {
    var cookie = {};
    //cookie= JSON.parse(cookie);

    elementC = document.cookie.split("; ")

    for (index = 0; index < elementC.length; index++) {
        app = elementC[index].split("=");
        cookie[app[0]] = app[1];
    }
    document.getElementById('welcome').value = "Benvenuto: " + cookie['username'];


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
