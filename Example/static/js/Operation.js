

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

