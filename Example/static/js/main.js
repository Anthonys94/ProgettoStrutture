var Url = 'http://127.0.0.1:5000';
/*
function onConnect(status) {
  if (status == Strophe.Status.CONNECTING) {
  } else if (status == Strophe.Status.CONNFAIL) {
	  alert('errore connessione fallita');
	  document.getElementById("btn").disabled=false;
    $('#connect').get(0).value = 'connect';
  }else if (status == Strophe.Status.AUTHFAIL){
	  alert('errore user o password errate');
	  document.getElementById("btn").disabled=false;
  } else if (status == Strophe.Status.CONNECTED) {
    //log('Strophe is connected.');
	  var input = $('.validate-input .input100');
    
	  $(input[1]).parent().addClass('corretto').text('Login in corso...').fadeTo(900, 1, function() {
			// al termine effettuo il redirect alla pagina privata
			var url = "chat.html?user="+ encodeURIComponent(connection.jid)+"&sid="+encodeURIComponent(connection._proto.sid)+"&rid="+encodeURIComponent(connection._proto.rid);
		   window.location.href = url;
		});
  }
}
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
  
  
    /*==================================================================*/



});