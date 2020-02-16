$('#GestioneProve').on('click', function () {
    var check = true;
    location.href = "GestioneProva.html";
    window.location.href = url;
});

$('#GestioneMateriali').on('click', function () {
    var check = true;
    location.href = "GestioneMateriali.html";
});

$('#GestioneStrutture').on('click', function () {
    var check = true;
    location.href = "GestioneStrutture.html";
});

$('#GestioneDocumenti').on('click', function () {
    var check = true;
    location.href = "GestioneDocumentiLeader.html";
});

$('#Query').on('click', function () {
    var check = true;
    location.href = "Ricerca_ad_Leader.html";
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
});


