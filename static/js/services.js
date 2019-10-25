
function get_experiencias(){
    console.log("Informacion del viajero");

    $.getJSON("/experiencias", function(data){
    var i=0;
    $.each(data, function(){
    console.log(data);
    id = data[i]['id'];
    titulo = data[i]['titulo'];
    descripcion = data[i]['descripcion'];
    precio = data[i]['precio'];
    fecha = data[i]['fecha'];
    calificacion = data[i]['calificacion'];
    guia = data[i]['guia'];
    e = '<div class="col-md-4 col-sm-4 col-xs-12" onclick="agregar_itinerario('+id+')" style="cursor:pointer;"><div class="service-widget"><div class="post-media wow fadeIn"><img src="/static/images/experiencias/'+titulo+'.png" alt="" class="img-responsive img-rounded"></div><h3>'+titulo+'</h3><p>'+descripcion+'</p><p>Price: '+precio+'$</p><p>Calificación: *'+calificacion+'*</p></div></div>'
    i = i+1;
    $("#servicios").append(e);
    })
        i = i+1;
    });
}

function agregar_itinerario(id_exp){

$.getJSON("/current", function(info){
    id_viaj = info['id']

var cont = JSON.stringify({
    "id_experiencia": id_exp,
    "id_viajero": id_viaj,
    "id_guia": "0"
    });
    $.ajax({
    url: '/itinerario',
    type: 'POST',
    contentType: 'aplication/json',
    data: cont,
    dataType: 'json'
 });
     });

     alert("Se ha agregado correctamente la experiencia #"+id_exp);
}