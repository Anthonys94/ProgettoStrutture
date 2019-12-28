  $('#ProvaHandle').on('click',function(){
    	var check = true;
       location.href= "FormInserimentoProva.html";
        window.location.href = url;
    });

  $('#MaterialeHandle').on('click',function(){
    	var check = true;
        location.href= "FormInserimentoMateriale.html";
    });

      $('#StrutturaHandle').on('click',function(){
    	var check = true;
        location.href = "FormInserimentoStruttura.html";
    });

      $('#addDocument').on('click',function(){
    	var check = true;
        location.href = "FormInserimentoDocumento.html";
    });


    $('#Query').on('click',function(){
    	var check = true;
        location.href = "ricerca.html";
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


