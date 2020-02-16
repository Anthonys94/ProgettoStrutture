var Url = 'http://127.0.0.1:5002';
var typingTimer;
var doneTypingInterval = 1500; //time in ms
var globalVariableStrutture;
var globalVariableProva;
var globalVariableMateriale;
var globalLetters;

function checkNamePdf(filename){
    var split_s = filename.split('.');
    if (split_s.length > 2 || split_s.length == 1) {return false}
    if (split_s[1].toLowerCase() == 'pdf'){return true}
}
//on keyup, start the countdown

$('#NPratica').on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$('#NPratica').on('keydown', function () {
    clearTimeout(typingTimer);
    //annullo modifico campi documento
    document.getElementById('idModificaDocumento').hidden = true;

    //annulla modifica foglio
    document.getElementById('idDowload').hidden = true;
    document.getElementById('idDowloadApertura').hidden = true;
    document.getElementById('btnFoglio').hidden = true;
    document.getElementById('btnFoglioApertura').hidden = true;
    document.getElementById('foglioLavoro').value = "";

    //aggiungi certificato
    document.getElementById('btnAggiungiCertificato').hidden = true;
    //nascondo tasto btnUpload
    document.getElementById('btnUpload').hidden = true;
    resetCertificati();
    var table = document.getElementById("TableDesc");
    var lun = table.rows.length;
    for (index = 1; index < lun; index++) {
        table.deleteRow(1);
    }
    //annulla
    document.getElementById('btnAnnulla').hidden = true;

    //sezioni
    document.getElementById('idSezModificaCampi').hidden = true;
    document.getElementById('idSezFoglioLavoro').hidden = true;
    document.getElementById('idSezCertificato').hidden = true;
    document.getElementById('idSezFoglioApertura').hidden = true;


});

function doneTyping() {
    if (document.getElementById('NPratica').value != "") {
        $.ajax({
            url: Url + "/check_esistenza",
            type: "GET",
            data: {
                NumeroPratica: document.getElementById('NPratica').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    document.getElementById('idModificaDocumento').hidden = false;
                    document.getElementById('btnFoglio').hidden = false;
                    document.getElementById('btnAggiungiCertificato').hidden = false;
                    document.getElementById('btnAnnulla').hidden = false;
                    document.getElementById('btnFoglioApertura').hidden = false;
                } else {
                    alert('Pratica non esistente');

                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    }

}

function successotrovaDocumento(result) {
    console.log(result)
    document.getElementById('idCommittente').value = result['committente'];
    document.getElementById('idDescrizione').value = result['descrizione'];
    document.getElementById('IdNewLuogo').value = result['altroLuogo'];
    document.getElementById('DataPratica').value = result['data'];
    document.getElementById('ListaProvince').value = result['provincia'];
    var comune = result['comune'];
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
                select.value = comune;
            }, error: function (xhr) {
                console.log("Error ${xhr}");
            }
        });
    }

}

function SuccessUpdateDocumento(result) {
    if (result['check'] == true) {
        document.getElementById('idCommittente').value = "";
        document.getElementById('idDescrizione').value = "";
        document.getElementById('IdNewLuogo').value = "";
        document.getElementById('DataPratica').value = "";
        document.getElementById('ListaProvince').value = "";
        document.getElementById("ListaComuni").value = "";
        document.getElementById('idSezModificaCampi').hidden = true;

    } else {
        alert('Errore durante la modifica')
    }

};

function successotrovaFoglioLavoro(result) {
    if (result['lavori_name'] != "") {
        document.getElementById('idDowload').hidden = false;
        document.getElementById('idpdfLavoro').value = result['lavori_name'];
    } else {
        document.getElementById('idDowload').hidden = true;
        document.getElementById('idpdfLavoro').value = "Foglio non presente";
    }
}

function successotrovaFoglioAperturaPratica(result){
    if (result['apertura_name'] != "") {
        document.getElementById('idDowloadApertura').hidden = false;
        document.getElementById('idpdfApertura').value = result['apertura_name'];
    } else {
        document.getElementById('idDowloadApertura').hidden = true;
        document.getElementById('idpdfApertura').value = "Foglio non presente";
    }
}

function submit_form_foglio() {
    var file = document.getElementById('foglioLavoro').value;
    if (file != "" && checkNamePdf(file)) {
        document.getElementById('praticaforPost').value = document.getElementById('NPratica').value;
        $.ajax({
            url: Url + "/ModificaFoglioLavoro",
            type: "POST",
            data: new FormData(document.getElementById('UploadNewFoglio')),
            contentType: false,
            processData: false,
            success: successoUploadFoglio
        });
    } else {
        alert('Inserire un nuovo foglio di lavoro in formato pdf.')
    }
}

function submit_form_foglioApertura() {
        var file = document.getElementById('foglioAperturaPratica').value;
    if (file != "" && checkNamePdf(file)) {
        document.getElementById('AperturapraticaforPost').value = document.getElementById('NPratica').value;
        $.ajax({
            url: Url + "/ModificaFoglioApertura",
            type: "POST",
            data: new FormData(document.getElementById('UploadNewFoglioApertura')),
            contentType: false,
            processData: false,
            success: successoUploadFoglioApertura
        });
    } else {
        alert('Inserire un nuovo foglio di lavoro in formato pdf.')
    }

}

function successoUploadFoglio(result) {
    if (result['check'] == true) {
        alert('File caricato con successo');
        document.getElementById('idDowload').hidden = true;
        document.getElementById('idSezFoglioLavoro').hidden = true;
        document.getElementById('foglioLavoro').value = "";
    } else {
        alert('Errore nel caricamento del file');
    }
}

function successoUploadFoglioApertura(result) {
    if (result['check'] == true) {
        alert('File caricato con successo');
        document.getElementById('idDowloadApertura').hidden = true;
        document.getElementById('idSezFoglioApertura').hidden = true;
        document.getElementById('foglioAperturaPratica').value = "";
    } else {
        alert('Errore nel caricamento del file');
    }
}

function successoGetCertificati(result) {
    globalLetters = [];
    var table = document.getElementById("TableDesc");
    var lun = result.length;
    for (index = 0; index < lun; index++) {
        var row = table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var third = row.insertCell(2);
        var fourth = row.insertCell(3)
        fistCell.append(document.createTextNode(result[index]['_id']));
        secondCell.append(document.createTextNode(result[index]['struttura']));
        third.append(document.createTextNode(result[index]['materiale']));
        fourth.append(document.createTextNode(result[index]['prova']));
        if (lun > 1 && result[index]['_id'].split('/').length > 1){
            globalLetters.push(result[index]['_id'].split('/')[1]);
        }

    }
}

function successoUploadCertificato(result) {
    if (result['check'] == true) {
        alert('Certificati aggiunti con successo');

        document.getElementById('btnUpload').hidden = true;
        resetCertificati();
        document.getElementById('idSezCertificato').hidden = true;
        var table = document.getElementById("TableDesc");
        var lun = table.rows.length;
        for (index = 1; index < lun; index++) {
            table.deleteRow(1);
        }
    } else {
        alert("Errore durante l'aggiunta dei certificati");
    }
}

// bottoni alle operazioni
$('#btnAnnulla').on('click', function () {
    document.getElementById('idModificaDocumento').hidden = true;
    document.getElementById('btnFoglio').hidden = true;
    document.getElementById('btnFoglioApertura').hidden = true;
    document.getElementById('btnAggiungiCertificato').hidden = true;
    document.getElementById('btnAnnulla').hidden = true;

    document.getElementById('NPratica').value = "";
    document.getElementById('idDowload').hidden = true;
    document.getElementById('foglioLavoro').value = "";
    document.getElementById('idDowloadApertura').hidden = true;
    document.getElementById('foglioAperturaPratica').value = "";

    document.getElementById('idSezModificaCampi').hidden = true;
    document.getElementById('idSezFoglioLavoro').hidden = true;
    document.getElementById('idSezCertificato').hidden = true;
    document.getElementById('idSezFoglioApertura').hidden = true;

    //nascondo tasto btnUpload
    document.getElementById('btnUpload').hidden = true;
    resetCertificati();
    var table = document.getElementById("TableDesc");
    var lun = table.rows.length;
    for (index = 1; index < lun; index++) {
        table.deleteRow(1);
    }


});

$('#idModificaDocumento').on('click', function () {
    document.getElementById('idDowload').hidden = true;
    document.getElementById('foglioLavoro').value = "";

    document.getElementById('idSezModificaCampi').hidden = false;
    document.getElementById('idSezFoglioLavoro').hidden = true;
    document.getElementById('idSezCertificato').hidden = true;

    //nascondo tasto btnUpload
    document.getElementById('btnUpload').hidden = true;
    resetCertificati();
    var table = document.getElementById("TableDesc");
    var lun = table.rows.length;
    for (index = 1; index < lun; index++) {
        table.deleteRow(1);
    }

    if (document.getElementById('NPratica').value != "") {
        //trova il documento
        $.ajax({
            url: Url + "/trovaDocumento",
            type: "GET",
            data: {
                NumeroPratica: document.getElementById('NPratica').value
            },
            success: successotrovaDocumento,
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }
});

$('#btnAggiungiCertificato').on('click', function () {
    document.getElementById('idDowload').hidden = true;
    document.getElementById('foglioLavoro').value = "";

    document.getElementById('idSezModificaCampi').hidden = true;
    document.getElementById('idSezFoglioLavoro').hidden = true;
    document.getElementById('idSezCertificato').hidden = false;

    //nascondo tasto btnUpload
    document.getElementById('btnUpload').hidden = true;
    resetCertificati();
    var table = document.getElementById("TableDesc");
    var lun = table.rows.length;
    for (index = 1; index < lun; index++) {
        table.deleteRow(1);
    }

    if (document.getElementById('NPratica').value != "") {
        //trova il documento
        $.ajax({
            url: Url + "/GetCertificati",
            type: "GET",
            data: {
                NumeroPratica: document.getElementById('NPratica').value
            },
            success: successoGetCertificati,
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }


});

$('#btnFoglio').on('click', function () {
    document.getElementById('idDowload').hidden = true;
    document.getElementById('foglioLavoro').value = "";

    document.getElementById('idSezModificaCampi').hidden = true;
    document.getElementById('idSezFoglioLavoro').hidden = false;
    document.getElementById('idSezCertificato').hidden = true;
    document.getElementById('idSezFoglioApertura').hidden = true;

    //nascondo tasto btnUpload
    document.getElementById('btnUpload').hidden = true;
    resetCertificati();
    var table = document.getElementById("TableDesc");
    var lun = table.rows.length;
    for (index = 1; index < lun; index++) {
        table.deleteRow(1);
    }

    if (document.getElementById('NPratica').value != "") {
        $.ajax({
            url: Url + "/trovaFoglioLavoro",
            type: "GET",
            data: {
                NumeroPratica: document.getElementById('NPratica').value
            },
            success: successotrovaFoglioLavoro,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    }

});

$('#btnFoglioApertura').on('click', function(){
    document.getElementById('idSezModificaCampi').hidden = true;
    document.getElementById('idSezFoglioLavoro').hidden = true;
    document.getElementById('idSezCertificato').hidden = true;
    document.getElementById('idSezFoglioApertura').hidden = false;

    document.getElementById('idDowloadApertura').hidden = true;
    document.getElementById('foglioAperturaPratica').value = "";

    //nascondo tasto btnUpload
    document.getElementById('btnUpload').hidden = true;
    resetCertificati();

    var table = document.getElementById("TableDesc");
    var lun = table.rows.length;
    for (index = 1; index < lun; index++) {
        table.deleteRow(1);
    }

    if (document.getElementById('NPratica').value != "") {
        $.ajax({
            url: Url + "/trovaFoglioApertura",
            type: "GET",
            data: {
                NumeroPratica: document.getElementById('NPratica').value
            },
            success: successotrovaFoglioAperturaPratica,
            error: function (error) {
                console.log("Error ${error}");
            }
        });
    }

});

//Bottoni per gli upload
$('#idAggiorna').on('click', function () {
    var richiesta = window.confirm("Sicuro di voler modificare il documento? L'operazione non è reversibile");
    if (richiesta) {
        if (document.getElementById('NPratica').value == "" ||
            document.getElementById('DataPratica').value == "" ||
            document.getElementById('idCommittente').value == "" ||
            document.getElementById('ListaProvince').value == "" ||
            document.getElementById('ListaComuni').value == "") {
            alert('Inserire tutti i campi obbligatori')
        } else {
            var date = new Date(document.getElementById('DataPratica').value);
            currentDate = new Date();
            if (currentDate < date) {
                alert('Formato di data errato');
            } else {
                $.ajax({
                    type: 'PUT',
                    url: Url + '/UpdateDocumento',
                    data: {
                        NumeroPratica: document.getElementById('NPratica').value,
                        committente: document.getElementById('idCommittente').value,
                        descrizione: document.getElementById('idDescrizione').value,
                        altroLuogo: document.getElementById('IdNewLuogo').value,
                        data: document.getElementById('DataPratica').value,
                        provincia: document.getElementById('ListaProvince').value,
                        comune: document.getElementById("ListaComuni").value
                    },
                    success: SuccessUpdateDocumento,
                    error: function (error) {
                        console.log("Error ${error}");
                    }

                });
            }


        }

    }
});

$('#idDowload').on('click', function () {

    $.ajax({
        url: Url + "/download",
        type: "GET",
        data: {
            file: document.getElementById('idpdfLavoro').value,
        },
        success: function (response, status, xhr) {
            // check for a filename
            var filename = "";
            var disposition = xhr.getResponseHeader('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
            }

            var type = xhr.getResponseHeader('Content-Type');
            var blob = new Blob([response], {type: type});

            if (typeof window.navigator.msSaveBlob !== 'undefined') {
                // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                window.navigator.msSaveBlob(blob, filename);
            } else {
                var URL = window.URL || window.webkitURL;
                var downloadUrl = URL.createObjectURL(blob);

                if (filename) {
                    // use HTML5 a[download] attribute to specify filename
                    var a = document.createElement("a");
                    // safari doesn't support this yet
                    if (typeof a.download === 'undefined') {
                        window.location = downloadUrl;
                    } else {
                        a.href = downloadUrl;
                        a.download = filename;
                        document.body.appendChild(a);
                        a.click();
                    }
                } else {
                    window.location = downloadUrl;
                }

                setTimeout(function () {
                    URL.revokeObjectURL(downloadUrl);
                }, 100); // cleanup
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });
});

$('#idDowloadApertura').on('click', function () {

    $.ajax({
        url: Url + "/download",
        type: "GET",
        data: {
            file: document.getElementById('idpdfApertura').value,
        },
        success: function (response, status, xhr) {
            // check for a filename
            var filename = "";
            var disposition = xhr.getResponseHeader('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
            }

            var type = xhr.getResponseHeader('Content-Type');
            var blob = new Blob([response], {type: type});

            if (typeof window.navigator.msSaveBlob !== 'undefined') {
                // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                window.navigator.msSaveBlob(blob, filename);
            } else {
                var URL = window.URL || window.webkitURL;
                var downloadUrl = URL.createObjectURL(blob);

                if (filename) {
                    // use HTML5 a[download] attribute to specify filename
                    var a = document.createElement("a");
                    // safari doesn't support this yet
                    if (typeof a.download === 'undefined') {
                        window.location = downloadUrl;
                    } else {
                        a.href = downloadUrl;
                        a.download = filename;
                        document.body.appendChild(a);
                        a.click();
                    }
                } else {
                    window.location = downloadUrl;
                }

                setTimeout(function () {
                    URL.revokeObjectURL(downloadUrl);
                }, 100); // cleanup
            }
        },
        error: function (error) {
            console.log("Error ${error}");
        }
    });
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

$('#btnUpload').on('click', function () {
    var numero = document.getElementById('NCertificati').value;
    var Nopdf = false;
    var enalbeUpload = true;
    for (index = 0; index < numero; index++) {
        var file = document.getElementById("f_Certificato" + String(index)).value;
        if (file == "" || !(file.toLowerCase().includes('.pdf'))) {
            enalbeUpload = false;
            Nopdf = true;
        }
    }
    if (Nopdf == true) {
        alert('Caricare file in formato pdf. Inserire almeno un prova!')
    }

    var missed = false;
    if (enalbeUpload == true) {
        for (index = 0; index < numero; index++) {
            if (document.getElementById('TipoStruttura' + String(index)).value == "" ||
                document.getElementById('TipoMateriale' + String(index)).value == "" ||
                document.getElementById('TipoMaProva' + String(index)).value == "" ||
                document.getElementById("Lettera" + String(index)).value == "") {
                enalbeUpload = false;
                missed = true;
            }
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
            if (array.includes(app) || globalLetters.includes(app)) {
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

    if (enalbeUpload == true) {
        document.getElementById('praticaforCert').value = document.getElementById('NPratica').value;
        $.ajax({
            url: Url + "/NuovoCertificato",
            type: "POST",
            data: new FormData(document.getElementById('idForm')),
            contentType: false,
            processData: false,
            success: successoUploadCertificato
        });
    }


});

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
    document.getElementById('NCertificati').value = "";
    document.getElementById('btnUpload').hidden = true;

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
