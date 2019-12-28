var Url = 'http://127.0.0.1:5000';

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


function successDeleteDocument(result){
    console.log(result)
    if (result['esito']== false){
        alert('Documento non esistente')
    }
    else{
        window.location.href = "/home.html";
    }

}

$('#btnDelete').on('click', function (){
    if (document.getElementById("NPratica").value==""){
        alert('Inserire il numero di pratica')
    }else{
        $.ajax({
        url: Url+"/DeleteDocument",
        type: "POST",
        data:{
            Pratica: document.getElementById("NPratica").value
        },
        success: successDeleteDocument,
        error: function(error){
            console.log("Error ${error}");
        }
    });
    }



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
