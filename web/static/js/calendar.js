function info_viajero(){

    console.log("Informacion del viajero");

    $.getJSON("/current", function(data){
    console.log(data);
    var i=0;
    id = data['id']
    nombre = data['nombre'];
    apellido = data['apellido'];
    usuario = data['usuario'];
    edad = data['edad'];
    pais = data['pais'];
    e = '<tr><th scope="row">'+nombre+'</th><td>'+apellido+'</td><td>'+usuario+'</td><td>'+edad+'</td><td>'+pais+'</td></tr>';
    i = i+1;
    $("#info_usuario").append(e);

    f = '<button type="button" class="btn btn-warning" onclick="get_experiencias('+id+')">Traer Experiencias</button>'
    $("#boton").append(f);

    });
}


function get_experiencias(id_viaj){
    console.log("Trayendo experiencias");
    var url = "/itinerario/"+id_viaj;
    $.getJSON(url,function(data){
    var i=0;
    console.log(data);
    id_exp = data['id_experiencia'];
    console.log(id_exp);

    $.each(data,function(){
    id_exp = data[i]['id_experiencia'];

    $.getJSON("/experiencias/"+id_exp,function(exp){
    console.log(exp);
    fecha = exp['fecha'];
    titulo = exp['titulo'];
    descripcion = exp['descripcion'];
    calificacion = exp['calificacion'];

    e = '<tr><th scope="row">'+fecha+'</th><td>'+titulo+'</td><td>'+descripcion+'</td><td>'+calificacion+'</td></tr>';
    $("#experiencias").append(e);
    });
    i = i+1;
    });
    });
}

