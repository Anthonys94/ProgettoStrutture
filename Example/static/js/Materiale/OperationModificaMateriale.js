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
    document.getElementById('spanNewD').hidden = true;
    document.getElementById('NewDescrizione').value = "";
    document.getElementById('NewDescrizione').hidden = true;
    document.getElementById('DescrizioneMateriale').hidden = true;

    document.getElementById('spanNewS').hidden = true;
    document.getElementById('NewMateriale').hidden = true;
    document.getElementById('NewMateriale').value = "";
    document.getElementById('CodiceMateriale').hidden = true;


    document.getElementById('ModificaTipoMateriale').value = "Modifica";
    document.getElementById('ModificaTipoMateriale').hidden = true;
    document.getElementById('SendNewMateriale').hidden = true;


});

function doneTyping() {
    $.ajax({
        url: Url + "/check_esistenza_materiale",
        type: "GET",
        data: {
            Materiale: document.getElementById('TipMateriale').value
        },
        success: function (result) {
            if (result['esito'] == true) {
                document.getElementById('ModificaTipoMateriale').hidden = false;
            } else {
                alert('Materiale non esistente');
                document.getElementById('ModificaTipoMateriale').hidden = true;
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });

}

function successGetSingleMateriale(result) {
    document.getElementById('ModificaTipoMateriale').value = "Annulla";

    if (result['esito'] == true) {
        document.getElementById('spanNewS').hidden = false;
        document.getElementById('spanNewD').hidden = false;

        document.getElementById('NewMateriale').hidden = false;
        document.getElementById('CodiceMateriale').hidden = false;

        document.getElementById('DescrizioneMateriale').hidden = false;
        document.getElementById('NewDescrizione').hidden = false;

        document.getElementById('NewMateriale').value = result['id'];
        document.getElementById('NewDescrizione').value = result['descr'];


        document.getElementById('SendNewMateriale').hidden = false;

    } else {
        alert('Si è verificato un problema')
    }

}

function submit_new_element() {
    if (document.getElementById('NewMateriale').value == "") {
        alert('Campo Identificativo obbligatorio')
    } else {
        $.ajax({
            url: Url + "/ModificaMateriale.html",
            type: "POST",
            data: new FormData(document.getElementById('Form')),
            contentType: false,
            processData: false,
            success: successoModificaMateriale
        });
    }

}

function successoModificaMateriale(result){
    if(result['check'] == true){
        alert('Elemento modificato con successo');
        var check = true;
        location.href = "GestioneMateriali.html"
    }else{
        alert("Errore durante la modifica")
    }

}
function submit_form() {
    if (document.getElementById('ModificaTipoMateriale').value == 'Modifica') {
        $.ajax({
            url: Url + "/get_single_materiale",
            type: "GET",
            data: {
                Materiale: document.getElementById('TipMateriale').value
            },
            success: successGetSingleMateriale,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    } else {
        document.getElementById('spanNewD').hidden = true;
        document.getElementById('NewDescrizione').value = "";
        document.getElementById('NewDescrizione').hidden = true;
        document.getElementById('DescrizioneMateriale').hidden = true;

        document.getElementById('spanNewS').hidden = true;
        document.getElementById('NewMateriale').hidden = true;
        document.getElementById('NewMateriale').value = "";
        document.getElementById('CodiceMateriale').hidden = true;


        document.getElementById('ModificaTipoMateriale').value = "Modifica";
        document.getElementById('SendNewMateriale').hidden = true;


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
        url: Url + "/getMaterialeWithDesc",
        type: "GET",
        success: successMateriale,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

});