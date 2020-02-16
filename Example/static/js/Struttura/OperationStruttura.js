var Url = 'http://127.0.0.1:5002';

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

function submit_form() {
    if (document.getElementById('TipStruttura').value != "") {
        $.ajax({
            url: Url + "/check_esistenza_struttura",
            type: "GET",
            data: {
                Struttura: document.getElementById('TipStruttura').value
            },
            success: addstruttura,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    } else {
        alert('Identificativo nullo')
    }

}

function addstruttura(result) {
    if (result['esito'] == true) {
        alert('Stuttura esistente');
    } else {
        if (document.getElementById('TipStruttura').value != "") {
            $.ajax({
                url: Url + "/FormInserimentoStruttura.html",
                type: "POST",
                data: new FormData(document.getElementById('Form')),
                contentType: false,
                processData: false,
                success: successAddStruttura
            });
        } else {
            alert('Identificativo nullo')
        }


    }

}

function successAddStruttura(result) {
    if (result['check'] == true) {
        alert('Elemento aggiunto con successo');
        var check = true;
        location.href = "GestioneStrutture.html";
    } else {
        alert("Errore durante l'inserimento");
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
        url: Url + "/getStruttureWithDesc",
        type: "GET",
        success: successStuttura,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

});