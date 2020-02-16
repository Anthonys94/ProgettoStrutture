var Url = 'http://127.0.0.1:5002';
var typingTimer;
var doneTypingInterval = 1500;  //time in ms

//on keyup, start the countdown
$('#NPratica').on('keyup', function () {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$('#NPratica').on('keydown', function () {
  clearTimeout(typingTimer);
  document.getElementById('btnElimina').hidden = true;
});

function doneTyping () {
    if (document.getElementById('NPratica').value !=""){
         $.ajax({
        url: Url+"/check_esistenza",
        type: "GET",
        data : {
            NumeroPratica: document.getElementById('NPratica').value
        },
        success: function(result){
            if (result['esito'] == true){
                document.getElementById('btnElimina').hidden = false;
            }else{
                alert('Pratica non esistente');

            }
        },
        error: function(error){
            console.log("Error ${error}");
        }
    });
    }

}

function submit_form(){
    var richiesta = window.confirm("Sicuro di voler eliminare ? L'operazione non è reversibile");
    if (richiesta) {
        $.ajax({
            url: Url + "/DeleteDocument",
            type: "GET",
            data: {
                Pratica: document.getElementById('NPratica').value
            },
            success: function (result) {
                if (result['esito'] == true) {
                    alert('Documento eliminato');
                     location.href= "GestioneDocumento.html";
                     window.location.href = url;
                } else {
                    alert("Errore durante l'eliminazione del documento");

                }
            },
            error: function (error) {
                console.log("Error ${error}");
            }
        });

    }
}

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