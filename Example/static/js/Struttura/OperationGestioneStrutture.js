  $('#NuovaStruttura').on('click',function(){
    	var check = true;
       location.href= "FormInserimentoStruttura.html";
        window.location.href = url;
    });

  $('#EliminaStruttura').on('click',function(){
    	var check = true;
       location.href= "EliminaStruttura.html";
        window.location.href = url;
    });

    $('#ModificaStruttura').on('click',function(){
    	var check = true;
       location.href= "ModificaStruttura.html";
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