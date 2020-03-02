var Url = 'http://127.0.0.1:5002';
//UPDATE RUOLO UTENTE
var typingTimerup;
var doneTypingIntervalup = 3000;  //time in ms

$('#idCodFisUp').on('keyup', function () {
    clearTimeout(typingTimerup);
    typingTimerup = setTimeout(doneTypingUpdate, doneTypingIntervalup);
});

$('#idCodFisUp').on('keydown', function () {
    clearTimeout(typingTimerup);
    document.getElementById("btnUpdate").hidden = true;
    document.getElementById("RuoloUp").hidden = true;
    document.getElementById("SezScadeUp").hidden = true;

});

function doneTypingUpdate() {
    if (document.getElementById('idCodFisUp').value != "") {
        $.ajax({
            url: Url + "/check_esistenza_utente_attivo",
            type: "GET",
            data: {
                CF: document.getElementById('idCodFisUp').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    document.getElementById("btnUpdate").hidden = false;
                    document.getElementById("RuoloUp").hidden = false;
                    document.getElementById("SezScadeUp").hidden = false;

                } else {
                    alert('Utente non esistente oppure non attivo');
                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }


}

function submit_form_Update_Utente() {
    $.ajax({
        type: 'PUT',
        url: Url + '/updateUtente',
        data: {
            CF: document.getElementById("idCodFisUp").value,
            ruolo: document.getElementById("ListaRuoliUP").value,
            Scade: document.getElementById("ScadeUP").checked
        },
        success: successUpdateRole,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

}

function successUpdateRole(result) {
    if (result['check'] == true) {

        alert("Utente Aggiornato");
        var check = true;
        location.href = "GestioneUtente.html";
        /*
        document.getElementById("UpdateDiv").hidden = true;
        table = document.getElementById("TableAttivi")
        righe = table.getElementsByTagName("tr");

        for (index = 1; index < righe.length; index++) {
            valore = righe[index].getElementsByTagName("td")[2]; //prendo il codice fiscale
            if (valore.innerText == document.getElementById("idCodFisUp").value) {
                var today = new Date();
                righe[index].getElementsByTagName("td")[1].innerText = document.getElementById("ListaRuoliUP").value;
                righe[index].getElementsByTagName("td")[2].innerText = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
                righe[index].getElementsByTagName("td")[3].innerText = document.getElementById("ScadeUP").checked;
            }
        }

        document.getElementById("btnUpdate").hidden = true;
        document.getElementById("RuoloUp").hidden = true;
        document.getElementById("bntAnnulla").hidden = true;
        document.getElementById("idCodFisUp").value = "";
        document.getElementById("SezScadeUp").hidden = true;

         */
    } else {
        alert("Errore durante l'aggiornamento ")
    }

}

function submit_form_add_Utente() {
    var enableUpload = true;
    if (document.getElementById('idNome').value == "" ||
        document.getElementById('idCognome').value == "" ||
        document.getElementById('ListaProvince').value == "" ||
        document.getElementById('ListaComuni').value == "" ||
        document.getElementById('DataDiNascita').value == "" ||
        document.getElementById('idPassword').value == "" ||
        document.getElementById('ListaRuoli').value == "" ||
        document.getElementById('idCodFis').value == "") {
        enableUpload = false;
    }

    if (enableUpload) {
        $.ajax({
            url: Url + "/check_esistenza_utente",
            type: "GET",
            data: {
                CF: document.getElementById('idCodFis').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    alert('Utente esistente');
                } else {
                    var date = new Date(document.getElementById('DataDiNascita').value);
                    currentDate = new Date();
                    if (currentDate < date) {
                        alert('Formato di data errato');
                    } else {
                        $.ajax({
                            type: 'POST',
                            url: Url + '/NewUtente',
                            data: {
                                Nome: document.getElementById("idNome").value,
                                Cognome: document.getElementById("idCognome").value,
                                Provincia: document.getElementById("ListaProvince").value,
                                Comune: document.getElementById("ListaComuni").value,
                                bday: document.getElementById("DataDiNascita").value,
                                CodiceFiscale: document.getElementById("idCodFis").value,
                                Password: document.getElementById("idPassword").value,
                                Ruolo: document.getElementById("ListaRuoli").value,
                                Scadenza: document.getElementById('Scade').checked

                            },
                            success: successAggiuntaUtente,
                            error: function (error) {
                                console.log("Error ${error}");
                            }
                        });
                    }

                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    } else {
        alert('Iserire tutti i campi');
    }
}

function successAggiuntaUtente(result) {
    console.log(result)
    if (result['check'] == true) {
        alert('Utente aggiunto');
        /*
        var table = document.getElementById("TableAttivi");
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var thirdcell = row.insertCell(2);
        var fourcell = row.insertCell(3);
        var today = new Date();
        fistCell.append(document.createTextNode(document.getElementById('idCodFis').value));
        secondCell.append(document.createTextNode(document.getElementById('ListaRuoli').value));
        thirdcell.append(document.createTextNode(today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate()));
        fourcell.append(document.createTextNode(document.getElementById('Scade').checked));

        document.getElementById("idForm").hidden = true;
        document.getElementById("bntAnnulla").hidden = true;

        document.getElementById('idNome').value = "";
        document.getElementById('idCognome').value = "";
        document.getElementById('ListaProvince').value = "";
        document.getElementById('ListaComuni').value = "";
        document.getElementById('DataDiNascita').value = "";
        document.getElementById('idPassword').value = "";
        document.getElementById('ListaRuoli').value = "";
        document.getElementById('idCodFis').value = "";
        document.getElementById('Scade').checked = true;

         */
        var check = true;
        location.href = "GestioneUtente.html";
    } else {
        alert("Errore nella creazione dell'utente");
    }
}

//RIATTIVAZIONE UTENTE
var typingTimerriat;
var doneTypingIntervalriat = 3000;  //time in ms
$('#idCodFisRiattiva').on('keyup', function () {
    clearTimeout(typingTimerriat);
    typingTimerriat = setTimeout(doneTypingIntervalRiatt, doneTypingIntervalriat);
});

$('#idCodFisRiattiva').on('keydown', function () {
    clearTimeout(typingTimerriat);
    document.getElementById('btnUpdateRiattiva').hidden = true;
    document.getElementById('SezScadeR').hidden = true;
});

function doneTypingIntervalRiatt() {
    if (document.getElementById("idCodFisRiattiva").value != "") {
        $.ajax({
            url: Url + "/check_esistenza_utente_inattivo",
            type: "GET",
            data: {
                CF: document.getElementById('idCodFisRiattiva').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    document.getElementById('btnUpdateRiattiva').hidden = false;
                    document.getElementById('SezScadeR').hidden = false;
                } else {
                    alert('Utente già attivo oppure non esistente');
                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }

}

function submit_form_Riatt_Utente() {
    $.ajax({
        type: 'PUT',
        url: Url + '/RiattivaUtente',
        data: {
            CF: document.getElementById("idCodFisRiattiva").value,
        },
        success: successRiattivazioneUtente,
        error: function (error) {
            console.log("Error ${error}");
        }
    });
}

function successRiattivazioneUtente(result) {
    if (result['check'] == true) {
        alert("Utente Riattivato");
        var check = true;
        location.href = "GestioneUtente.html";
        /*
        var ruolo;
        table = document.getElementById("TableNonAttivi")
        righe = table.getElementsByTagName("tr");
        for (index = 1; index < righe.length; index++) {
            valore = righe[index].getElementsByTagName("td")[0]; //prendo il codice fiscale
            if (valore.innerText.toUpperCase() == document.getElementById('idCodFisRiattiva').value) {
                ruolo = righe[index].getElementsByTagName("td")[1];
                table.deleteRow(index);
            }
        }
        var today = new Date();
        table = document.getElementById("TableAttivi");
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var thirdcell = row.insertCell(2);
        var fourcell = row.insertCell(3);
        fistCell.append(document.createTextNode(document.getElementById('idCodFisRiattiva').value.toUpperCase()));
        secondCell.append(document.createTextNode(ruolo.innerText));
        thirdcell.append(document.createTextNode(today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate()));
        fourcell.append(document.createTextNode(document.getElementById('ScadeR').checked));

        document.getElementById('idCodFisRiattiva').value = "";

        document.getElementById("riattivaUtente").hidden = true;
        document.getElementById("btnUpdateRiattiva").hidden = true;
        document.getElementById('SezScadeR').hidden = true;
        document.getElementById("bntAnnulla").hidden = true;
        */

    } else {
        alert("Errore nella riattivazione dell'utente");
    }




}

//DISATTIVAZIONE UTENTE
var typingTimerDis;
var doneTypingIntervaldis = 1500;  //time in ms
$('#idCodFisDisattiva').on('keyup', function () {
    clearTimeout(typingTimerDis);
    typingTimerDis = setTimeout(doneTypingIntervalDis, doneTypingIntervaldis);
});

$('#idCodFisDisattiva').on('keydown', function () {
    clearTimeout(typingTimerDis);
    document.getElementById('btnUpdateRiattiva').hidden = true;
    document.getElementById('SezScadeR').hidden = true;
});

function doneTypingIntervalDis() {
    if (document.getElementById('idCodFisDisattiva').value != "") {
        $.ajax({
            url: Url + "/check_esistenza_utente_attivo",
            type: "GET",
            data: {
                CF: document.getElementById('idCodFisDisattiva').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    document.getElementById("btnUpdateDisattiva").hidden = false;
                } else {
                    alert('Utente non esistente oppure non attivo');
                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }

}

function submit_form_Disattiva_Utente() {
    $.ajax({
        type: 'PUT',
        url: Url + '/DisattivaUtente',
        data: {
            CF: document.getElementById("idCodFisDisattiva").value,
        },
        success: successDisattivaUtente,
        error: function (error) {
            console.log("Error ${error}");
        }
    });


}

function successDisattivaUtente(result) {
    if (result['check'] == true) {
        alert('Utente disattivato');
        var check = true;
        location.href = "GestioneUtente.html";
        /*
        var ruolo;
        var data;
        table = document.getElementById("TableAttivi")
        righe = table.getElementsByTagName("tr");
        for (index = 1; index < righe.length; index++) {
            valore = righe[index].getElementsByTagName("td")[0]; //prendo il codice fiscale
            if (valore.innerText == document.getElementById('idCodFisDisattiva').value) {
                ruolo = righe[index].getElementsByTagName("td")[1];
                data = righe[index].getElementsByTagName("td")[2];

                table.deleteRow(index);
            }
        }
        var today = new Date();
        table = document.getElementById("TableNonAttivi");
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var thirdcell = row.insertCell(2);
        fistCell.append(document.createTextNode(document.getElementById('idCodFisDisattiva').value));
        secondCell.append(document.createTextNode(ruolo.innerText));
        thirdcell.append(document.createTextNode(data.innerText));

        document.getElementById('idCodFisDisattiva').value = "";
        document.getElementById('btnUpdateRiattiva').hidden = true;
        document.getElementById('disattivaUtente').hidden = true;
        document.getElementById("bntAnnulla").hidden = true;

         */
    } else {
        alert("Errore nella disattivazione dell'utente")
    }
}

//----------------------------------------
$("#bntNewUtente").on('click', function (ev) {
    document.getElementById("UpdateDiv").hidden = true;
    document.getElementById("idForm").hidden = false;
    document.getElementById("bntAnnulla").hidden = false;
    document.getElementById("riattivaUtente").hidden = true;
    document.getElementById("UtentiAttivi").hidden = true;
    document.getElementById("UtentiNonAttivi").hidden = true;
    document.getElementById("disattivaUtente").hidden = true;
});

$("#bntUpdateUtente").on('click', function (ev) {
    document.getElementById("idForm").hidden = true;
    document.getElementById("riattivaUtente").hidden = true;
    document.getElementById("UpdateDiv").hidden = false;
    document.getElementById("bntAnnulla").hidden = false;
    document.getElementById("UtentiAttivi").hidden = true;
    document.getElementById("UtentiNonAttivi").hidden = true;
    document.getElementById("disattivaUtente").hidden = true;
});

$("#bntAttivaUtente").on('click', function (ev) {
    document.getElementById("idForm").hidden = true;
    document.getElementById("riattivaUtente").hidden = false;
    document.getElementById("UpdateDiv").hidden = true;
    document.getElementById("bntAnnulla").hidden = false;
    document.getElementById("UtentiAttivi").hidden = true;
    document.getElementById("UtentiNonAttivi").hidden = true;
    document.getElementById("disattivaUtente").hidden = true;
});

$("#bntDisattivaUtente").on('click', function (ev) {
    document.getElementById("idForm").hidden = true;
    document.getElementById("riattivaUtente").hidden = true;
    document.getElementById("UpdateDiv").hidden = true;
    document.getElementById("bntAnnulla").hidden = false;
    document.getElementById("UtentiAttivi").hidden = true;
    document.getElementById("UtentiNonAttivi").hidden = true;
    document.getElementById("disattivaUtente").hidden = false;

});

$("#bntAnnulla").on('click', function (ev) {
    document.getElementById("idForm").hidden = true;
    document.getElementById("UpdateDiv").hidden = true;
    document.getElementById("bntAnnulla").hidden = true;
    document.getElementById("riattivaUtente").hidden = true;
    document.getElementById("UtentiAttivi").hidden = true;
    document.getElementById("UtentiNonAttivi").hidden = true;
    document.getElementById("disattivaUtente").hidden = true;
});

$("#mostraAttivi").on('click', function (ev) {
    document.getElementById("idForm").hidden = true;
    document.getElementById("UpdateDiv").hidden = true;
    document.getElementById("bntAnnulla").hidden = false;
    document.getElementById("riattivaUtente").hidden = true;
    document.getElementById("UtentiAttivi").hidden = false;
    document.getElementById("UtentiNonAttivi").hidden = true;
    document.getElementById("disattivaUtente").hidden = true;
});

$("#mostraNonAttivi").on('click', function (ev) {
    document.getElementById("idForm").hidden = true;
    document.getElementById("UpdateDiv").hidden = true;
    document.getElementById("bntAnnulla").hidden = false;
    document.getElementById("riattivaUtente").hidden = true;
    document.getElementById("UtentiAttivi").hidden = true;
    document.getElementById("UtentiNonAttivi").hidden = false;
    document.getElementById("disattivaUtente").hidden = true;
});
//----------------------------------------

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

function successGetUtenti(result) {
    console.log(result)
    var Attivi = result['Attivi'];
    var Scaduti = result['Scaduti'];

    var table = document.getElementById("TableAttivi");
    var lun = Attivi.length;
    for (index = 0; index < lun; index++) {
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var thirdcell = row.insertCell(2);
        var fourcell = row.insertCell(3);

        fistCell.append(document.createTextNode(Attivi[index]['cf']));
        secondCell.append(document.createTextNode(Attivi[index]['ruolo']));
        thirdcell.append(document.createTextNode(Attivi[index]['dataInserimento']));
        fourcell.append(document.createTextNode(Attivi[index]['scadenza']));
    }

    var table = document.getElementById("TableNonAttivi");
    var lun = Scaduti.length;
    for (index = 0; index < lun; index++) {
        var row = table.insertRow(-1);

        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var thirdcell = row.insertCell(2);

        fistCell.append(document.createTextNode(Scaduti[index]['cf']));
        secondCell.append(document.createTextNode(Scaduti[index]['ruolo']));
        thirdcell.append(document.createTextNode(Scaduti[index]['dataInserimento']));

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
    //provincia
    $.ajax({
        url: Url + "/getProvince",
        type: "GET",
        success: successGetProvince,
        error: function (error) {
            console.log("Error ${error}");
        }
    });
    //Utenti
    $.ajax({
        url: Url + "/getUtenti",
        type: "GET",
        success: successGetUtenti,
        error: function (error) {
            console.log("Error ${error}");
        }
    });

});