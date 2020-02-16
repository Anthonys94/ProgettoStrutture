var Url = 'http://127.0.0.1:5002';
var typingTimer;
var doneTypingInterval = 1500;  //time in ms

//on keyup, start the countdown
$('#TipMateriale').on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$('#TipMateriale').on('keydown', function () {
    clearTimeout(typingTimer);
    document.getElementById('delTipoMateriale').hidden = true;
});

function doneTyping() {
    if (document.getElementById('TipMateriale').value != "") {
        $.ajax({
            url: Url + "/check_esistenza_materiale",
            type: "GET",
            data: {
                Materiale: document.getElementById('TipMateriale').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    document.getElementById('delTipoMateriale').hidden = false;
                } else {
                    alert('Materiale non esistente');
                    document.getElementById('delTipoMateriale').hidden = true;
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
            url: Url + "/deleteMateriale",
            type: "GET",
            data: {
                elemento: document.getElementById('TipMateriale').value
            },
            success: successoEliminaMateriale
        });
    }
}

function successoEliminaMateriale(result) {
    if (result['check'] == true) {
        alert('Elemento eliminato');
        var check = true;
        location.href = "GestioneMateriali.html";
    } else {
        alert("Errore durante l'eliminazione")
    }
}

function successMateriale(result) {
    var table = document.getElementById("TableDesc");
    var lun = result.length
    for (index = 0; index < lun; index++) {
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        fistCell.append(document.createTextNode(result[index]['materiale']));
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
        url: Url + "/getMaterialeWithDesc",
        type: "GET",
        success: successMateriale,
        error: function (error) {
            console.log("Error ${error}");
        }
    });
});