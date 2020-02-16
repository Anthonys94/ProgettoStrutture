var globalVariableStrutture;
var globalVariableProva;
var globalVariableMateriale;
var typingTimer;
var doneTypingInterval = 1500;  //time in ms
var Url = 'http://127.0.0.1:5002';

//on keyup, start the countdown
/*
$('#NPratica').on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});
*/
/*
//on keydown, clear the countdown
$('#NPratica').on('keydown', function () {
    clearTimeout(typingTimer);
    document.getElementById('btnUpload').hidden = true;
    if (!document.getElementById('NCertificati').value == "" && !isNaN(document.getElementById('NCertificati').value)) {
        var numero = parseInt(document.getElementById('NCertificati').value);
        for (index = 0; index < numero; index++) {
            //elimino tutti i campi sotto
            var element = document.getElementById("Certificato" + String(index));
            element.parentNode.removeChild(element);
        }
        document.getElementById('bntNCertificat').textContent = "Inserisci Certificati";
        document.getElementById('NCertificati').readOnly = false;
        document.getElementById('btnUpload').hidden = true;
        document.getElementById('NCertificati').value = "";
    }

});
*/

/*
function doneTyping() {
    $.ajax({
        url: Url + "/check_esistenza",
        type: "GET",
        data: {
            NumeroPratica: document.getElementById('NPratica').value
        },
        success: function (result) {
            if (result['esito'] == true) {
                alert('Pratica esistente');
                enablebtn = false;
            } else {
                enablebtn = true;
                if (!document.getElementById('NCertificati').value == "" && !isNaN(document.getElementById('NCertificati').value)) {
                    var incipit = document.getElementById('idForm');
                    document.getElementById('btnUpload').hidden = false;
                    incipit.append(document.getElementById('btnUpload'));
                }
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });
}
*/

function successStrutture(result) {
    globalVariableStrutture = result;
}

function successMateriale(result) {
    globalVariableMateriale = result;
}

function successProva(result) {
    globalVariableProva = result;
}

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

function aggiungiCertificati() {
    var numero = parseInt(document.getElementById('NCertificati').value);
    var incipit = document.getElementById('idForm');
    for (index = 0; index < numero; index++) {
        var div = document.createElement("div");
        div.class = "wrap-input100 validate-input m-t-85 m-b-35";
        div.id = "Certificato" + String(index);
        // STRUTTURA
        var txtStruttura = document.createElement("input");
        txtStruttura.class = "input100";
        txtStruttura.value = "Inserire Struttura*:";
        txtStruttura.readOnly = true;
        div.append(txtStruttura);
        var select = document.createElement("select");
        select.required = true;
        select.id = 'TipoStruttura' + String(index);
        select.name = "Struttura" + String(index);
        var option = document.createElement("option");
        option.value = "";
        option.text = "Scegli Struttura";
        option.selected = true;
        option.disabled = true;
        select.appendChild(option);
        var lung = globalVariableStrutture.length;
        for (step = 0; step < lung; step++) {
            var option = document.createElement("option");
            option.value = globalVariableStrutture[step]["tipologiaStruttura"];
            option.text = globalVariableStrutture[step]["tipologiaStruttura"];
            select.appendChild(option);
        }

        div.append(select);
        div.append(document.createElement("br"));
        // MATERIALE
        var txtMateriale = document.createElement("input");
        txtMateriale.class = "input100";
        txtMateriale.value = "Inserire Materiale*:";
        txtMateriale.readOnly = true;
        div.append(txtMateriale);
        var select = document.createElement("select");
        select.required = true;
        select.id = 'TipoMateriale' + String(index);
        select.name = "Materiale" + String(index);
        var option = document.createElement("option");
        option.value = "";
        option.text = "Scegli Materiale";
        option.selected = true;
        option.disabled = true;
        select.appendChild(option);
        var lung = globalVariableMateriale.length;
        for (step = 0; step < lung; step++) {
            var option = document.createElement("option");
            option.value = globalVariableMateriale[step]["materiale"];
            option.text = globalVariableMateriale[step]["materiale"];
            select.appendChild(option);
        }

        div.append(select);
        div.append(document.createElement("br"));
        //PROVA
        var txtProva = document.createElement("input");
        txtProva.class = "input100";
        txtProva.value = "Inserire Prova*:";
        txtProva.readOnly = true;
        div.append(txtProva);
        var select = document.createElement("select");
        select.required = true;
        select.id = 'TipoMaProva' + String(index);
        select.name = "Prova" + String(index);
        var option = document.createElement("option");
        option.value = "";
        option.text = "Scegli Prova";
        option.selected = true;
        option.disabled = true;
        select.appendChild(option);
        var lung = globalVariableProva.length;
        for (step = 0; step < lung; step++) {
            var option = document.createElement("option");
            option.value = globalVariableProva[step]["tipoProva"];
            option.text = globalVariableProva[step]["tipoProva"];
            select.appendChild(option);
        }
        div.append(select);
        div.append(document.createElement("br"));
        var upload = document.createElement("input");
        upload.name = "Certificato" + String(index);
        upload.id = "f_Certificato" + String(index);
        upload.type = "file";
        upload.required = true;


        if (numero > 1) {
            var input = document.createElement("input");
            input.name = "Lettera" + String(index);
            input.type = "text";
            input.required = true;
            input.id = "Lettera" + String(index);
            //input.style.border = "thick solid #FFFFFF";
            var txt = document.createElement("input");
            txt.class = "input100";
            txt.value = "Inserire Lettera*";
            txt.readOnly = true;
            div.append(txt);
            div.append(input);
        }

        div.append(upload);
        incipit.append(div);
        div.append(document.createElement("br"));
        div.append(document.createElement("br"));


    }
    document.getElementById('bntNCertificat').textContent = "Reset";
    document.getElementById('NCertificati').readOnly = true;
    document.getElementById('btnUpload').hidden = false;
    incipit.append(document.getElementById('btnUpload'));


}

function resetCertificati() {
    var numero = parseInt(document.getElementById('NCertificati').value);
    for (index = 0; index < numero; index++) {
        //elimino tutti i campi sotto
        var element = document.getElementById("Certificato" + String(index));
        element.parentNode.removeChild(element);
    }
    document.getElementById('bntNCertificat').textContent = "Inserisci Certificati";
    document.getElementById('NCertificati').readOnly = false;
    document.getElementById('btnUpload').hidden = true;

}

function checkNamePdf(filename){
    var split_s = filename.split('.');
    if (split_s.length > 2 || split_s.length == 1) {return false}
    if (split_s[1].toLowerCase() == 'pdf'){return true}
}

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

$('.input100').each(function () {
    $(this).on('blur', function () {
        if ($(this).val().trim() != "") {
            $(this).addClass('has-val');
        } else {
            $(this).removeClass('has-val');
        }
    })
});

$('#bntNCertificat').on('click', function () {
    if (isNaN(document.getElementById('NCertificati').value) ||
        document.getElementById('NCertificati').value == "") {
        alert("Numero dei certificati deve essere un numero");
    } else {
        if (document.getElementById('bntNCertificat').textContent == "Inserisci Certificati") {
            aggiungiCertificati();
        } else {
            resetCertificati();

        }

    }

});

function submit_form() {
    $.ajax({
        url: Url + "/check_esistenza",
        type: "GET",
        data: {
            NumeroPratica: document.getElementById('NPratica').value
        },
        success: function (result) {
            if (result['esito'] == true) {
                alert('Impossibile cariare il documento! Pratica esistente');
            } else {
                tryUpload()
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });

};

function tryUpload() {
    var enalbeUpload = true;
    var numero = parseInt(document.getElementById('NCertificati').value);
    for (index = 0; index < numero; index++) {
        var file = document.getElementById("f_Certificato" + String(index)).value;
        if (file == "" || !(checkNamePdf(file))) {
            enalbeUpload = false;
        }
    }
    if (enalbeUpload == true) {
        var file_apertura = document.getElementById('aperturaPratica').value;
        var file_lavoro = document.getElementById('foglioLavoro').value;
        if (!(file_apertura == "") && !(checkNamePdf(file_apertura))) {
            enalbeUpload = false;
        }
        if (!(file_lavoro == "") && !(checkNamePdf(file_lavoro))) {
            enalbeUpload = false;
        }
    }
    if (enalbeUpload == false) {
        alert('Caricare file in formato pdf. Inserire almeno un prova!')
    }
    //controllo sui campi
    if (enalbeUpload == true) {
        if (document.getElementById('NPratica').value == "" || document.getElementById('DataPratica').value == "" ||
            document.getElementById('idCommittente').value == "" ||
            document.getElementById('ListaProvince').value == "" || document.getElementById('ListaComuni').value == "") {
            enalbeUpload = false;
            alert('Inserire tutti i campi obbligatori')
        }
    }
    if (enalbeUpload == true) {
        var date = new Date(document.getElementById('DataPratica').value);
        currentDate = new Date();
        if (currentDate < date) {
            enalbeUpload = false;
            alert('Formato di data errato');
        }
    }
    if (enalbeUpload == true) {
        if (numero > 1) {
            var missed = false;
            for (index = 0; index < numero; index++) {
                if (document.getElementById('TipoStruttura' + String(index)).value == "" ||
                    document.getElementById('TipoMateriale' + String(index)).value == "" ||
                    document.getElementById('TipoMaProva' + String(index)).value == "" ||
                    document.getElementById("Lettera" + String(index)).value == "") {
                    enalbeUpload = false;
                    missed = true;
                }
            }

            if (missed == true) {
                alert('Inserire tutti i campi obbligatori')
            }

            var invalid = false;
            if (enalbeUpload == true) {
                for (index = 0; index < numero; index++) {
                    var app = document.getElementById("Lettera" + String(index)).value;
                    if (!isNaN(app) || app.length > 1) {
                        enalbeUpload = false;
                        invalid = true;
                    }
                }
            }
            if (invalid == true) {
                alert('Inserire solo una Lettera')
            }
            if (enalbeUpload == true) {
                var array = [];
                var duplicato = false;
                for (index = 0; index < numero; index++) {
                    var app = document.getElementById("Lettera" + String(index)).value.toUpperCase();
                    if (array.includes(app)) {
                        enalbeUpload = false;
                        duplicato = true;
                    } else {
                        array.push(app);
                    }

                }

            }
            if (duplicato == true) {
                alert('Lettera già in uso');
            }

        } else {
            if (document.getElementById('TipoStruttura' + String(0)).value == "" ||
                document.getElementById('TipoMateriale' + String(0)).value == "" ||
                document.getElementById('TipoMaProva' + String(0)).value == "") {
                enalbeUpload = false;
                alert('Inserire tutti i campi obbligatori')
            }

        }


    }
    if (enalbeUpload == true) {
        //$('#idForm').submit();
        $.ajax({
            url: Url + "/FormInserimentoDocumento.html",
            type: "POST",
            data: new FormData(document.getElementById('idForm')),
            contentType: false,
            processData: false,
            success: successoUploadCertificato
        });
    }


}

function successoUploadCertificato(result) {
    if (result['check'] == true) {
        alert('Inserimento avvenuto con successo');
        var check = true;
        location.href = "GestioneDocumento.html";

    } else {
        alert("Errore durante l'inserimento")
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

    $.ajax({
        url: Url + "/getStrutture",
        type: "GET",
        success: successStrutture,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url + "/getProva",
        type: "GET",
        success: successProva,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

    $.ajax({
        url: Url + "/getMateriale",
        type: "GET",
        success: successMateriale,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

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
