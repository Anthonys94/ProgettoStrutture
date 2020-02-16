  $('#NuovoDocumento').on('click',function(){
    	var check = true;
       location.href= "FormInserimentoDocumento.html";
        window.location.href = url;
    });


  $('#ModificaDocumento').on('click',function(){
    	var check = true;
        location.href= "ModificaDocumento.html";
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


