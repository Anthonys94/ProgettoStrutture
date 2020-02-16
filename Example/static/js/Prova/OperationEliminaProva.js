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
    document.getElementById('delTipoProva').hidden = true;
});

function doneTyping() {
    if (document.getElementById('TipProva').value != "") {
        $.ajax({
            url: Url + "/check_esistenza_prova",
            type: "GET",
            data: {
                Prova: document.getElementById('TipProva').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    document.getElementById('delTipoProva').hidden = false;
                } else {
                    alert('Prova non esistente');
                    document.getElementById('delTipoProva').hidden = true;
                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }


}


function submit_form() {
    var richiesta = window.confirm("Sicuro di voler eliminare ? L'operazione non è reversibile");
    if (richiesta) {
        $.ajax({
            url: Url + "/deleteProva",
            type: "GET",
            data: {
                esito: document.getElementById('TipProva').value
            },
            success: successoEliminaProva
        });
    }
}

function successoEliminaProva(result) {
    if (result['check'] == true) {
        alert('Elemento eliminato');
        var check = true;
        location.href = "GestioneProva.html";
    } else {
        alert("Errore durante l'eliminazione")
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
    })
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