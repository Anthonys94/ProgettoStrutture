var Url = 'http://127.0.0.1:5002';

function doneTyping() {
    $.ajax({
        url: Url + "/check_esistenza_prova",
        type: "GET",
        data: {
            Prova: document.getElementById('TipProva').value
        },
        success: function (result) {
            if (result['esito'] == true) {
                alert('Prova esistente');
                document.getElementById('addTipoProva').hidden = true;
            } else {
                document.getElementById('addTipoProva').hidden = false;
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });

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

function submit_form() {
    if (document.getElementById('TipProva').value != "") {
        $.ajax({
            url: Url + "/check_esistenza_prova",
            type: "GET",
            data: {
                Prova: document.getElementById('TipProva').value
            },
            success: addProva,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    }
}

function addProva(result) {
    if (result['esito'] == true) {
        alert('Prova esistente');
    } else {
        if (document.getElementById('TipProva').value != "") {
            $.ajax({
                url: Url + "/FormInserimentoProva.html",
                type: "POST",
                data: new FormData(document.getElementById('newProva')),
                contentType: false,
                processData: false,
                success: successAddProva
            });
        } else {
            alert('Identificativo nullo')
        }
    }
}

function successAddProva(result) {
    if (result['check'] == true) {
        alert('Elemento aggiunto con successo');
        var check = true;
        location.href = "GestioneProva.html";
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

    elementC = document.cookie.split("; ")

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