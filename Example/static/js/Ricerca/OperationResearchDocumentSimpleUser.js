var Url = 'http://127.0.0.1:5002';
var globalVariableStrutture;
var globalVariableProva;
var globalVariableMateriale;

function successStrutture(result){
    globalVariableStrutture = result;
    // aggiungi le strutture
    var lung = globalVariableStrutture.length;
    var select = document.getElementById("ListaStrutture");
    for (step = 0; step < lung; step++){
        var option = document.createElement("option");
        option.value = globalVariableStrutture[step]["tipologiaStruttura"];
        option.text= globalVariableStrutture[step]["tipologiaStruttura"];
        select.appendChild(option);
    }
}

function successMateriale(result){
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

function successProva(result){
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

function successGetProvince(result){
    var lung = result.length;
    var select = document.getElementById("ListaProvince");
    for (step = 0; step < lung; step++){
        var option = document.createElement("option");
        option.value = result[step]["provincia"];
        option.text= result[step]["provincia"];
        select.appendChild(option);
            }
}

function successQuerybyPratica(result){
    console.log(result)
    document.getElementById('RicercaNumeroPratica').hidden = true;
    document.getElementById('Annulla').hidden = true;
    document.getElementById("Result").value = 'La tua ricerca ha prodotto ' + result['num'] + ' risultati';
    document.getElementById("DivResult").hidden=false;
}

function successQuerybyCampo(result){
    console.log(result)
    document.getElementById('RicercaperCampi').hidden = true;
    document.getElementById('Annulla').hidden = true;
    document.getElementById("Result").value = 'La tua ricerca ha prodotto ' + result['num'] + ' risultati';
    document.getElementById("DivResult").hidden=false;
}

$("#ListaProvince").change(function() {
    console.log(document.getElementById("ListaProvince").value);
    // chiamare i comuni
    var select = document.getElementById("ListaComuni");
    select.options.length = 0;
    var option = document.createElement("option");
    option.value = "";
    option.text= "Scegli Comune";
    option.selected = true;
    select.appendChild(option);
    if (document.getElementById("ListaProvince").value != ""){
            $.ajax({
        url: Url+"/getComuni",
        type: "get", //send it through get method
        data: {
            provincia: document.getElementById("ListaProvince").value
        },
        success: function(response) {
            var lung = response.length;
            var select = document.getElementById("ListaComuni");
            for (step = 0; step < lung; step++){
                var option = document.createElement("option");
                option.value = response[step]["comune"];
                option.text= response[step]["comune"];
                select.appendChild(option);
            }
            },
        error: function(xhr) {
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

$('.input100').each(function(){
    $(this).on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
            }
        })
    });

$('#bntNewRicercaPratica').on('click', function () {
   document.getElementById('RicercaNumeroPratica').hidden = false;
   document.getElementById('RicercaperCampi').hidden = true;
   document.getElementById('Annulla').hidden = false;
   document.getElementById("DivResult").hidden=true;
});

$('#bntNewRicercaCampo').on('click', function () {
    document.getElementById('RicercaNumeroPratica').hidden = true;
    document.getElementById('RicercaperCampi').hidden = false;
    document.getElementById('Annulla').hidden = false;
    document.getElementById("DivResult").hidden=true;


});

$('#Annulla').on('click', function () {
    document.getElementById('RicercaNumeroPratica').hidden = true;
    document.getElementById('RicercaperCampi').hidden = true;
    document.getElementById('Annulla').hidden = true;
    document.getElementById("DivResult").hidden=true;
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

$(document).ready(function(){
    var cookie = {};
    //cookie= JSON.parse(cookie);

    elementC = document.cookie.split("; ")

    for(index=0; index<elementC.length; index++){
        app = elementC[index].split("=");
        cookie[app[0]] = app[1];
    }
    document.getElementById('welcome').value = "Benvenuto: " + cookie['username'];

    $.ajax({
        url: Url+"/getStrutture",
        type: "GET",
        success: successStrutture,
        error: function(error){
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url+"/getProva",
        type: "GET",
        success: successProva,
        error: function(error){
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url+"/getMateriale",
        type: "GET",
        success: successMateriale,
        error: function(error){
            console.log("Error ${error}");
        }
    });


    //province
        $.ajax({
        url: Url+"/getProvince",
        type: "GET",
        success: successGetProvince,
        error: function(error){
            console.log("Error ${error}");
        }
    });

});
