  $('#NuovoMateriale').on('click',function(){
    	var check = true;
       location.href= "FormInserimentoMateriale.html";
        window.location.href = url;
    });

  $('#EliminaMateriale').on('click',function(){
    	var check = true;
       location.href= "EliminaMateriale.html";
        window.location.href = url;
    });

    $('#ModificaMateriale').on('click',function(){
    	var check = true;
       location.href= "ModificaMateriale.html";
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