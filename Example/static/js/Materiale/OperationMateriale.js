var Url = 'http://127.0.0.1:5002';


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

function submit_form() {
    if (document.getElementById('TipMateriale').value != "") {
        $.ajax({
            url: Url + "/check_esistenza_materiale",
            type: "GET",
            data: {
                Materiale: document.getElementById('TipMateriale').value
            },
            success: addMateriale,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    } else {
        alert('Identificativo nullo')
    }

}

function addMateriale(result) {
    if (result['esito'] == true) {
        alert('Materiale esistente');
    } else {
        if (document.getElementById('TipMateriale').value != "") {
            $.ajax({
                url: Url + "/FormInserimentoMateriale.html",
                type: "POST",
                data: new FormData(document.getElementById('Form')),
                contentType: false,
                processData: false,
                success: successAddMateriale
            });
        } else {
            alert('Identificativo nullo')
        }
    }
}

function successAddMateriale(result) {
    if (result['check'] == true) {
        alert('Elemento aggiunto con successo');
        var check = true;
        location.href = "GestioneMateriali.html";
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
        url: Url + "/getMaterialeWithDesc",
        type: "GET",
        success: successMateriale,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

});