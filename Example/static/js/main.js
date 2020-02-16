var Url = 'http://127.0.0.1:5000';
/*
function SuccessLogin(result){
    $.ajax({
        url: Url+"/home.html",
        type: "GET",
        success: function sucesso(result) {
            console.log('ok');
        },
        error: function(error){
            console.log("Error ${error}");
        }
    });

};


$('#btn').on('click', function (){
     $.ajax({
        url: Url+"/",
        type: "POST",
         data: {
            Username: document.getElementById("email").value,
             pass: document.getElementById("pass").value
        },
        success: SuccessLogin,
        error: function(error){
            console.log("Error ${error}");
        }
    });
});
*/
$(document).ready(function(){



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
  


});