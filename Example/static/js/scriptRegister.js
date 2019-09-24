var server = 'studenti';
var BOSH_SERVICE = 'http://127.0.0.1:7070/http-bind/';
var ROOM = 'prova@conference.' + server;
var ROOM_SERVICE = 'conference.' + server;
var connection = null;




function rawInput(data) {
  console.log('RECV: ' + data);
}

function rawOutput(data) {
  console.log('SENT: ' + data);
}

function register() {
	var registerCallback = function (status) {
		if (status === Strophe.Status.REGISTER) {
			console.log("registerCallback: REGISTER");
			connection.register.fields.username = $('#jid').get(0).value;
			connection.register.fields.password = $('#pass').get(0).value;
			console.log(connection.register.fields);
			connection.register.submit();
		} else if (status === Strophe.Status.REGISTERED) {
			console.log("registerCallback: REGISTERED");
			$('#jid').get(0).value = $('#jid').get(0).value + "@" + server;
			$('#pass').get(0).value = $('#pass').get(0).value;
			connection.authenticate();
			
		} else if (status === Strophe.Status.CONNECTED) {
			console.log("registerCallback: CONNECTED");
			// set presence
			connection.send($pres());
			var url = "chat.html?user="+ encodeURIComponent(connection.jid)+"&sid="+encodeURIComponent(connection._proto.sid)+"&rid="+encodeURIComponent(connection._proto.rid);
			window.location.href = url;
			//updateConnButton(true);
		} else if (status === Strophe.Status.CONFLICT) {
			console.log("registerCallback: Contact already existed!");
			 alert('Contact already existed');
			$('#register').attr('disabled',false);
		} else if (status === Strophe.Status.NOTACCEPTABLE) {
			console.log("registerCallback: Registration form not properly filled out.")
			$('#register').attr('disabled',false);
		} else if (status === Strophe.Status.REGIFAIL) {
			console.log("registerCallback: The Server does not support In-Band Registration")
			$('#register').attr('disabled',false);
		} else {
			// every other status a connection.connect would receive
		}
	};
	connection = new Strophe.Connection(BOSH_SERVICE);
    connection.rawInput = rawInput;
    connection.rawOutput = rawOutput;
	connection.register.connect(server, registerCallback,60 ,1);
}

(function ($) {
    "use strict";

$('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })

$(document).ready(function() {
 // var input = $('.validate-input .input100');
  $("#register").bind('click', function () {
		var input = $('.validate-input .input100');
		var check = true;
		$('#register').attr('disabled',true);
        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }
		
		if(check==true)
        {
			/*var utente = $('#jid').get(0).value;
			var pass = $('#pass').get(0).value;
			if((utente.match(/[-!$%^&*()_+|~@=`{}\[\]:";'<>?,.\/]/) == null)&& pass != null)*/
				register();
			/*else
				$('#register').attr('disabled',false);*/
		}else{
			$('#register').attr('disabled',false);
		}
		return false;
	});
});


$('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    /*funzione validate per la texbox username e password, non permette che nel campo username si inserisano simboli e controlla che il campo password non sia vuoto*/
   function validate (input) {
        if($(input).attr('type') == 'username' || $(input).attr('name') == 'username') {
            if($(input).val().trim().match(/[^a-zA-Z0-9]+/) != null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    /*aggiunge la classe alert-validate, viene chiamata quando non è stato inserito il valore nella texbox*/
    function showValidate(input) {
        var thisAlert = $(input).parent();
        
        $(thisAlert).addClass('alert-validate');
        
    }
    
    
    /*rimuove la classe alert-validate quanso scrivo qualcosa*/
    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
	
})(jQuery);