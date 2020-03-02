var Url = 'http://127.0.0.1:5002';

function SuccessLogin(result){

    if (result['check'] == false){
        alert('Credenziali Invalide');
        var check = true;
        location.href = "/";
    }
};

/*
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
function submit_form(){
    $.ajax({
            url: Url + "/",
            type: "POST",
            data: new FormData(document.getElementById('idForm')),
            contentType: false,
            processData: false,
            success: SuccessLogin
        });
}
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