

$("#btnEmail").on('click', function (ev) {
    window.open('mailto:strutture@unina.it?subject=Richiesta Informazioni&body=Nome: Cognome: Codice Fiscale: Informazioni: ');
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
});