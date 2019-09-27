$('#btnNewLuogo').on('click',function(ev){
    ev.preventDefault();
    var ul = document.getElementById('ListaLuoghi');
    var li = document.createElement("li");
    var input = document.createElement("input");
    var testo = document.getElementById('newLuogo').value;
    input.value = testo;
    input.name ='Luoghi[]';
    input.type = 'text'
    //li.appendChild(document.createTextNode(testo));
    li.appendChild(input);
    ul.appendChild(li);
    document.getElementById('newLuogo').value = "";
});

$('#btnNewProvincia').on('click',function(ev){
    ev.preventDefault();
    var ul = document.getElementById('ListaProvince');
    var li = document.createElement("li");
    var input = document.createElement("input");
    var testo = document.getElementById('newProvincia').value
    input.value = testo;
    input.name ='Province[]';
    input.type = 'text'
    //li.appendChild(document.createTextNode(testo));
    li.appendChild(input);
    ul.appendChild(li);
    document.getElementById('newProvincia').value = "";
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

$(document).ready(function(){
    const Url = 'http://127.0.0.1:5000'
    $.ajax({
        url: Url+"/getStrutture",
        type: "GET",
        success: function(result){
            var lung = result.length;
            for (step = 0; step < lung; step++){

                var option = document.createElement("option");
                option.value = result[step]["tipologiaStruttura"];
                option.text= result[step]["tipologiaStruttura"];
                document.getElementById('idScegliStruttura').appendChild(option);
            }

        },
        error: function(error){
            console.log("Error ${error}");
        }
    })

    $.ajax({
        url: Url+"/getProva",
        type: "GET",
        success: function(result){
            var lung = result.length;
            for (step = 0; step < lung; step++){

                var option = document.createElement("option");
                option.value = result[step]["tipoProva"];
                option.text= result[step]["tipoProva"];
                document.getElementById('idScegliProva').appendChild(option);
            }

        },
        error: function(error){
            console.log("Error ${error}");
        }
    })

    $.ajax({
        url: Url+"/getMateriale",
        type: "GET",
        success: function(result){
            var lung = result.length;
            for (step = 0; step < lung; step++){

                var option = document.createElement("option");
                option.value = result[step]["materiale"];
                option.text= result[step]["materiale"];
                document.getElementById('idScegliMateriale').appendChild(option);
            }

        },
        error: function(error){
            console.log("Error ${error}");
        }
    })
});
