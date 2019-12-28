var Url = 'http://127.0.0.1:5000';

function successGetProvince(result){
    var lung = result.length;
    var select = document.getElementById("ListaProvince");
    for (step = 0; step < lung; step++){
        var option = document.createElement("option");
        option.value = result[step]["provincia"];
        option.text= result[step]["provincia"];
        select.appendChild(option);
            }
}

function successGetUtenti(result){
    //console.log(result)
    var Attivi = result['Attivi']
    var Scaduti = result['Scaduti']

    var table = document.getElementById("TableAttivi");
    var lun = Attivi.length
    for (index=0; index < lun; index++){
        var row =  table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var thirdcell = row.insertCell(2);
        var fourcell = row.insertCell(3);
        var fifthcell = row.insertCell(4);

        fistCell.append(document.createTextNode(Attivi[index]['nome']));
        secondCell.append(document.createTextNode(Attivi[index]['cognome']));
        thirdcell.append(document.createTextNode(Attivi[index]['cf']));
        fourcell.append(document.createTextNode(Attivi[index]['ruolo']));
        fifthcell.append(document.createTextNode(Attivi[index]['dataInserimento']));

    }
    var table = document.getElementById("TableNonAttivi");
    var lun = Scaduti.length
    for (index=0; index < lun; index++){
        var row =  table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        var thirdcell = row.insertCell(2);
        var fourcell = row.insertCell(3);
        var fifthcell = row.insertCell(4);

        fistCell.append(document.createTextNode(Scaduti[index]['nome']));
        secondCell.append(document.createTextNode(Scaduti[index]['cognome']));
        thirdcell.append(document.createTextNode(Scaduti[index]['cf']));
        fourcell.append(document.createTextNode(Scaduti[index]['ruolo']));
        fifthcell.append(document.createTextNode(Scaduti[index]['dataInserimento']));

    }
}

function successChekUtente(result){
    if (result['check']==true){
        document.getElementById("btnUpdate").hidden = false;
        document.getElementById("RuoloUp").hidden = false;
    }else{
        alert("L'utente non esiste oppure non è attivo");
    }

}

function successUpdateRole(result){
    document.getElementById("UpdateDiv").hidden=true;
    alert("Utente Aggiornato");

    table = document.getElementById("TableAttivi")
    righe = table.getElementsByTagName("tr");

    for (index=1; index<righe.length; index++){
        valore = righe[index].getElementsByTagName("td")[2]; //prendo il codice fiscale
        if (valore.innerText == document.getElementById("idCodFisUp").value){
            var today = new Date();
            righe[index].getElementsByTagName("td")[3].innerText = document.getElementById("ListaRuoliUP").value;
            righe[index].getElementsByTagName("td")[4].innerText = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        }
    }

    document.getElementById("btnUpdate").hidden = true;
    document.getElementById("RuoloUp").hidden = true;
    document.getElementById("bntAnnulla").hidden=true;

}

function successChekUtenteRiattiva(result){
     if (result['check']==true){
        document.getElementById("btnUpdateRiattiva").hidden = false;
        document.getElementById("RuoloRiattiva").hidden = false;
    }else{
        alert("L'utente non esiste oppure è ancora attivo");
    }
}

function successRiattivazioneUtente(result){
    document.getElementById("riattivaUtente").hidden=true;
    alert("Utente Riattivato");

    table = document.getElementById("TableAttivi");
    var row =  table.insertRow(-1);
    var fistCell = row.insertCell(0);
    var secondCell = row.insertCell(1);
    var thirdcell = row.insertCell(2);
    var fourcell = row.insertCell(3);
    var fifthcell = row.insertCell(4);

    fistCell.append(document.createTextNode(result['nome']));
    secondCell.append(document.createTextNode(result['cognome']));
    thirdcell.append(document.createTextNode(result['cf']));
    fourcell.append(document.createTextNode(result['ruolo']));
    fifthcell.append(document.createTextNode(result['dataInserimento']));

    table = document.getElementById("TableNonAttivi")
    righe = table.getElementsByTagName("tr");
    for (index=1; index<righe.length; index++){
        valore = righe[index].getElementsByTagName("td")[2]; //prendo il codice fiscale
        if (valore.innerText == result['cf']){
            table.deleteRow(index);
        }
    }
    document.getElementById("btnUpdateRiattiva").hidden = true;
    document.getElementById("RuoloRiattiva").hidden = true;
    document.getElementById("bntAnnulla").hidden=true;

}

function successAggiuntaUtente(result){
    if (result['check']==true) {
        document.getElementById("idForm").hidden=true;
        document.getElementById("bntAnnulla").hidden=true;
        location.href = "gestioneUtenze.html";
    }else{
        alert("Errore nella creazione dell'utente");
    }
}

$("#ListaProvince").change(function() {
    console.log(document.getElementById("ListaProvince").value);
    // chiamare i comuni
    var select = document.getElementById("ListaComuni");
    select.options.length = 0;
    var option = document.createElement("option");
    option.value = "";
    option.text= "Scegli Comune";
    option.selected = true;
    option.disabled = true;
    select.appendChild(option);
    if (document.getElementById("ListaProvince").value != ""){
            $.ajax({
        url: Url+"/getComuni",
        type: "get", //send it through get method
        data: {
            provincia: document.getElementById("ListaProvince").value
        },
        success: function(response) {
            var lung = response.length;
            var select = document.getElementById("ListaComuni");
            for (step = 0; step < lung; step++){
                var option = document.createElement("option");
                option.value = response[step]["comune"];
                option.text= response[step]["comune"];
                select.appendChild(option);
            }
            },
        error: function(xhr) {
            console.log("Error ${xhr}");
        }
});

    }

});

//----------------------------------------

$("#bntNewUtente").on('click',function(ev){
    document.getElementById("UpdateDiv").hidden=true;
    document.getElementById("idForm").hidden=false;
    document.getElementById("bntAnnulla").hidden=false;
    document.getElementById("riattivaUtente").hidden=true;
    document.getElementById("UtentiAttivi").hidden=true;
    document.getElementById("UtentiNonAttivi").hidden=true;
});

$("#bntUpdateUtente").on('click',function(ev){
    document.getElementById("idForm").hidden=true;
    document.getElementById("riattivaUtente").hidden=true;
    document.getElementById("UpdateDiv").hidden=false;
    document.getElementById("bntAnnulla").hidden=false;
    document.getElementById("UtentiAttivi").hidden=true;
    document.getElementById("UtentiNonAttivi").hidden=true;
});

$("#bntAttivaUtente").on('click',function(ev){
    document.getElementById("idForm").hidden=true;
    document.getElementById("riattivaUtente").hidden=false;
    document.getElementById("UpdateDiv").hidden=true;
    document.getElementById("bntAnnulla").hidden=false;
    document.getElementById("UtentiAttivi").hidden=true;
    document.getElementById("UtentiNonAttivi").hidden=true;
});

$("#bntAnnulla").on('click',function(ev){
    document.getElementById("idForm").hidden=true;
    document.getElementById("UpdateDiv").hidden=true;
    document.getElementById("bntAnnulla").hidden=true;
    document.getElementById("riattivaUtente").hidden=true;
    document.getElementById("UtentiAttivi").hidden=true;
    document.getElementById("UtentiNonAttivi").hidden=true;
});

$("#mostraAttivi").on('click',function(ev){
    document.getElementById("idForm").hidden=true;
    document.getElementById("UpdateDiv").hidden=true;
    document.getElementById("bntAnnulla").hidden=false;
    document.getElementById("riattivaUtente").hidden=true;
    document.getElementById("UtentiAttivi").hidden=false;
    document.getElementById("UtentiNonAttivi").hidden=true;
});

$("#mostraNonAttivi").on('click',function(ev){
    document.getElementById("idForm").hidden=true;
    document.getElementById("UpdateDiv").hidden=true;
    document.getElementById("bntAnnulla").hidden=false;
    document.getElementById("riattivaUtente").hidden=true;
    document.getElementById("UtentiAttivi").hidden=true;
    document.getElementById("UtentiNonAttivi").hidden=false;
});


//----------------------------------------
$("#bntesiste").on('click',function(ev){
        //Utenti
    $.ajax({
        url: Url+"/verificaUtente",
        type: "GET",
        data: {
            CF: document.getElementById("idCodFisUp").value
        },
        success: successChekUtente,
        error: function(error){
            console.log("Error ${error}");
        }
    });

});

$("#bntesisteRiattiva").on('click',function(ev){
        //Utenti
    $.ajax({
        url: Url+"/verificaUtenteInattivo",
        type: "GET",
        data: {
            CF: document.getElementById("idCodFisRiattiva").value
        },
        success: successChekUtenteRiattiva,
        error: function(error){
            console.log("Error ${error}");
        }
    });

});

$("#btnUpdate").on('click',function(ev){
     $.ajax({
        type: 'PUT',
        url: Url+'/updateUtente',
        data: {
            CF : document.getElementById("idCodFisUp").value,
            ruolo : document.getElementById("ListaRuoliUP").value
        },
        success: successUpdateRole,
         error: function(error){
            console.log("Error ${error}");
        }
    });
});

$("#btnUpdateRiattiva").on('click',function(ev){
     $.ajax({
        type: 'PUT',
        url:  Url+ '/RiattivaUtente',
        data: {
            CF : document.getElementById("idCodFisRiattiva").value,
            ruolo : document.getElementById("ListaRuoliRiattiva").value
        },
        success: successRiattivazioneUtente,
         error: function(error){
            console.log("Error ${error}");
        }
    });
});

$("#btnUpload").on('click',function(ev){
     $.ajax({
        type: 'POST',
        url:  Url+ '/gestioneUtenze.html',
        data: {
            Nome: document.getElementById("idNome").value,
            Cognome: document.getElementById("idCognome").value,
            Provincia: document.getElementById("ListaProvince").value,
            Comune: document.getElementById("ListaComuni").value,
            bday: document.getElementById("DataDiNascita").value,
            CodiceFiscale: document.getElementById("idCodFis").value,
            Password: document.getElementById("idPassword").value,
            Ruolo: document.getElementById("ListaRuoli").value

        },
        success: successAggiuntaUtente,
         error: function(error){
            console.log("Error ${error}");
        }
    });
});

$('.input100').each(function(){
    $(this).on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
        }
    })
    });

$(document).ready(function(){
        var cookie = {};
    //cookie= JSON.parse(cookie);

    elementC = document.cookie.split("; ")

    for(index=0; index<elementC.length; index++){
        app = elementC[index].split("=");
        cookie[app[0]] = app[1];
    }
    document.getElementById('welcome').value = "Benvenuto: " + cookie['username'];
    //provincia
    $.ajax({
        url: Url+"/getProvince",
        type: "GET",
        success: successGetProvince,
        error: function(error){
            console.log("Error ${error}");
        }
    });
    //Utenti
    $.ajax({
        url: Url+"/getUtenti",
        type: "GET",
        success: successGetUtenti,
        error: function(error){
            console.log("Error ${error}");
        }
    });


});