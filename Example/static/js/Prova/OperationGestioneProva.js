  $('#NuovaProva').on('click',function(){
    	var check = true;
       location.href= "FormInserimentoProva.html";
        window.location.href = url;
    });

  $('#EliminaProva').on('click',function(){
    	var check = true;
       location.href= "EliminaProva.html";
        window.location.href = url;
    });

    $('#ModificaProva').on('click',function(){
    	var check = true;
       location.href= "ModificaProva.html";
        window.location.href = url;
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