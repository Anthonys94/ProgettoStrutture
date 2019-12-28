var Url = 'http://127.0.0.1:5000';

function successProva(result){
    var table = document.getElementById("TableDesc");
    var lun = result.length
    for (index=0; index < lun; index++){
        var row =  table.insertRow(-1);
        var fistCell = row.insertCell(0);
        var secondCell = row.insertCell(1);
        fistCell.append(document.createTextNode(result[index]['tipoProva']));
        secondCell.append(document.createTextNode(result[index]['descrizione']))
    }

}
/*
function successAddProva(result){
    if (result['check']==true){
        Location.ref = "FormInserimentoProva.html"
    }else{
        alert("Tipologia prova già esistente");
    }

}


$("#newProva").on('click', function () {
     $.ajax({
        url: Url+"/FormInserimentoProva.html",
        type: "POST",
        data:{
            TipologiaProva: document.getElementById("TipProva").value,
            DescrizioneProva:document.getElementById("DescProva").value
        },
        success: successAddProva,
        error: function(error){
            console.log("Error ${error}");
        }
    });
});
*/
$(document).ready(function(){
    var cookie = {};
    //cookie= JSON.parse(cookie);

    elementC = document.cookie.split("; ")

    for(index=0; index<elementC.length; index++){
        app = elementC[index].split("=");
        cookie[app[0]] = app[1];
    }
    document.getElementById('welcome').value = "Benvenuto: " + cookie['username'];
    $.ajax({
        url: Url+"/getProvaWithDesc",
        type: "GET",
        success: successProva,
        error: function(error){
            console.log("Error ${error}");
        }
    });

});