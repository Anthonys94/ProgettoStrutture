var Url = 'http://127.0.0.1:5002';
var typingTimer;
var doneTypingInterval = 1500;  //time in ms

//on keyup, start the countdown
$('#TipStruttura').on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$('#TipStruttura').on('keydown', function () {
    clearTimeout(typingTimer);
    document.getElementById('spanNewD').hidden = true;
    document.getElementById('NewDescrizione').value = "";
    document.getElementById('NewDescrizione').hidden = true;
    document.getElementById('DescrizioneStrutt').hidden = true;

    document.getElementById('spanNewS').hidden = true;
    document.getElementById('NewStruttura').hidden = true;
    document.getElementById('NewStruttura').value = "";
    document.getElementById('CodiceStruttura').hidden = true;


    document.getElementById('ModificaTipoStruttura').value = "Modifica";
    document.getElementById('ModificaTipoStruttura').hidden = true;
    document.getElementById('SendNewStruttura').hidden = true;


});

function doneTyping() {
    $.ajax({
        url: Url + "/check_esistenza_struttura",
        type: "GET",
        data: {
            Struttura: document.getElementById('TipStruttura').value
        },
        success: function (result) {
            if (result['esito'] == true) {
                document.getElementById('ModificaTipoStruttura').hidden = false;
            } else {
                alert('Stuttura non esistente');
                document.getElementById('ModificaTipoStruttura').hidden = true;
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });

}

function successGetSingleStruttura(result) {
    document.getElementById('ModificaTipoStruttura').value = "Annulla";

    if (result['esito'] == true) {
        document.getElementById('spanNewS').hidden = false;
        document.getElementById('spanNewD').hidden = false;

        document.getElementById('NewStruttura').hidden = false;
        document.getElementById('CodiceStruttura').hidden = false;

        document.getElementById('DescrizioneStrutt').hidden = false;
        document.getElementById('NewDescrizione').hidden = false;

        document.getElementById('NewStruttura').value = result['id'];
        document.getElementById('NewDescrizione').value = result['descr'];


        document.getElementById('SendNewStruttura').hidden = false;

    } else {
        alert('Si è verificato un problema')
    }

}

function submit_new_element() {
    if (document.getElementById('NewStruttura').value == "") {
        alert('Campo Identificativo obbligatorio')
    } else {
        $.ajax({
            url: Url + "/ModificaStruttura.html",
            type: "POST",
            data: new FormData(document.getElementById('Form')),
            contentType: false,
            processData: false,
            success: successoModificaStruttura
        });
    }

}

function  successoModificaStruttura(result) {
    if(result['check'] == true){
        alert('Elemento modificato con successo');
        var check = true;
        location.href = "GestioneStrutture.html";
    }else{
        alert("Errore durante la modifica")
    }
}

function submit_form() {
    if (document.getElementById('ModificaTipoStruttura').value == 'Modifica') {
        $.ajax({
            url: Url + "/get_single_struttura",
            type: "GET",
            data: {
                Struttura: document.getElementById('TipStruttura').value
            },
            success: successGetSingleStruttura,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    } else {
        document.getElementById('spanNewD').hidden = true;
        document.getElementById('NewDescrizione').value = "";
        document.getElementById('NewDescrizione').hidden = true;
        document.getElementById('DescrizioneStrutt').hidden = true;

        document.getElementById('spanNewS').hidden = true;
        document.getElementById('NewStruttura').hidden = true;
        document.getElementById('NewStruttura').value = "";
        document.getElementById('CodiceStruttura').hidden = true;


        document.getElementById('ModificaTipoStruttura').value = "Modifica";
        document.getElementById('SendNewStruttura').hidden = true;


    }


}


function successStuttura(result) {
    var table = document.getElementById("TableDesc");
    var lun = result.length
    for (index = 0; index < lun; index++) {
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        fistCell.append(document.createTextNode(result[index]['tipologiaStruttura']));
        secondCell.append(document.createTextNode(result[index]['descrizione']))
    }

}


$('.input100').each(function () {
    $(this).on('blur', function () {
        if ($(this).val().trim() != "") {
            $(this).addClass('has-val');
        } else {
            $(this).removeClass('has-val');
        }
    });
});

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
        url: Url + "/getStruttureWithDesc",
        type: "GET",
        success: successStuttura,
        error: function (error) {
            console.log("Error ${error}");
        }
    });
});