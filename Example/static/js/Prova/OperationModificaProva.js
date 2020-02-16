var Url = 'http://127.0.0.1:5002';
var typingTimer;
var doneTypingInterval = 1500;  //time in ms

//on keyup, start the countdown
$('#TipProva').on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$('#TipProva').on('keydown', function () {
    clearTimeout(typingTimer);
    document.getElementById('spanNewD').hidden = true;
    document.getElementById('NewDescrizione').value = "";
    document.getElementById('NewDescrizione').hidden = true;
    document.getElementById('DescrizioneProva').hidden = true;

    document.getElementById('spanNewS').hidden = true;
    document.getElementById('NewProva').hidden = true;
    document.getElementById('NewProva').value = "";
    document.getElementById('CodiceProva').hidden = true;


    document.getElementById('ModificaTipoProva').value = "Modifica";
    document.getElementById('ModificaTipoProva').hidden = true;
    document.getElementById('SendNewProva').hidden = true;


});

function doneTyping() {
    $.ajax({
        url: Url + "/check_esistenza_prova",
        type: "GET",
        data: {
            Prova: document.getElementById('TipProva').value
        },
        success: function (result) {
            if (result['esito'] == true) {
                document.getElementById('ModificaTipoProva').hidden = false;
            } else {
                alert('Prova non esistente');
                document.getElementById('ModificaTipoProva').hidden = true;
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });

}

function successGetSingleProva(result) {
    document.getElementById('ModificaTipoProva').value = "Annulla";

    if (result['esito'] == true) {
        document.getElementById('spanNewS').hidden = false;
        document.getElementById('spanNewD').hidden = false;

        document.getElementById('NewProva').hidden = false;
        document.getElementById('CodiceProva').hidden = false;

        document.getElementById('DescrizioneProva').hidden = false;
        document.getElementById('NewDescrizione').hidden = false;

        document.getElementById('NewProva').value = result['id'];
        document.getElementById('NewDescrizione').value = result['descr'];


        document.getElementById('SendNewProva').hidden = false;

    } else {
        alert('Si è verificato un problema')
    }

}

function submit_new_element() {
    if (document.getElementById('NewProva').value == "") {
        alert('Campo Identificativo obbligatorio')
    } else {
        $.ajax({
            url: Url + "/ModificaProva.html",
            type: "POST",
            data: new FormData(document.getElementById('Form')),
            contentType: false,
            processData: false,
            success: successoModificaProva
        });
    }
}

function successoModificaProva(result) {
    if (result['check'] == true) {
        alert('Elemento modificato con successo');
        var check = true;
        location.href = "GestioneProva.html";
    } else {
        alert("Errore durante la modifica")
    }
}

function submit_form() {
    if (document.getElementById('ModificaTipoProva').value == 'Modifica') {
        $.ajax({
            url: Url + "/get_single_prova",
            type: "GET",
            data: {
                Prova: document.getElementById('TipProva').value
            },
            success: successGetSingleProva,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    } else {
        document.getElementById('spanNewD').hidden = true;
        document.getElementById('NewDescrizione').value = "";
        document.getElementById('NewDescrizione').hidden = true;
        document.getElementById('DescrizioneProva').hidden = true;

        document.getElementById('spanNewS').hidden = true;
        document.getElementById('NewProva').hidden = true;
        document.getElementById('NewProva').value = "";
        document.getElementById('CodiceProva').hidden = true;


        document.getElementById('ModificaTipoProva').value = "Modifica";
        document.getElementById('SendNewProva').hidden = true;


    }


}


function successProva(result) {
    var table = document.getElementById("TableDesc");
    var lun = result.length
    for (index = 0; index < lun; index++) {
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        fistCell.append(document.createTextNode(result[index]['tipoProva']));
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
        url: Url + "/getProvaWithDesc",
        type: "GET",
        success: successProva,
        error: function (error) {
            console.log("Error ${error}");
        }
    });


});