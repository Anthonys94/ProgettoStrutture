$('#GestioneProve').on('click', function () {
    var check = true;
    location.href = "GestioneProvaOperatore.html";
    window.location.href = url;
});

$('#GestioneMateriali').on('click', function () {
    var check = true;
    location.href = "GestioneMaterialiOperatore.html";
});

$('#GestioneStrutture').on('click', function () {
    var check = true;
    location.href = "GestioneStruttureOperatore.html";
});

$('#GestioneDocumenti').on('click', function () {
    var check = true;
    location.href = "GestioneDocumentoOperatore.html";
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


