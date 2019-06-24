var iconoMasculino = L.icon({
    iconUrl: '/static/img/iconos/masculino-mapa.png',
    shadowUrl: '/static/img/iconos/masculino-sombra-mapa.png',

    iconSize:     [25, 60], // size of the icon
    shadowSize:   [46, 31], // size of the shadow
    iconAnchor:   [12, 30], // point of the icon which will correspond to marker's location
    shadowAnchor: [10, 0],  // the same for the shadow
    popupAnchor:  [0, -30] // point from which the popup should open relative to the iconAnchor
});

var iconoFemenino = L.icon({
    iconUrl: '/static/img/iconos/femenino-mapa.png',
    shadowUrl: '/static/img/iconos/femenino-sombra-mapa.png',

    iconSize:     [31, 60], // size of the icon
    shadowSize:   [46, 31], // size of the shadow
    iconAnchor:   [15, 30], // point of the icon which will correspond to marker's location
    shadowAnchor: [10, 0],  // the same for the shadow
    popupAnchor:  [0, -30] // point from which the popup should open relative to the iconAnchor
});


$( window ).resize(function() {
  tamanio_mapa();
});


$(document).ready(function() {
	tamanio_mapa();

  // create a map in the "map" div, set the view to a given place and zoom
    var sudoeste = L.latLng(-20, -86);
    var noreste = L.latLng(-60, -36);
    var limites_mapa = L.latLngBounds(sudoeste, noreste);

  map = L.map('mapa',
              {
                minZoom: 4,
                maxZoom:13,
                maxBounds: limites_mapa
              }
              ).setView([-34.8, -58.7], 5);

  // add an OpenStreetMap tile layer
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  crear_consulta ();

    map.on('popupopen', function() {  
      $('.caso-popup').click(function(e){
          var id_caso = $(this).attr("id_caso");
          $.post( "/archivo/caso-json/", {
              id_caso: id_caso,
          }, function( data ) {
            $('#modal-caso .modal-content').html(data);
            $('#modal-caso').modal('toggle');
          });
          
      });
  });

    $(".caso-popup").click(function(){
      console.log("prueba popup");
      var id_caso = $(this).attr("id_caso");

      $.post( "/archivo/cargar-marcadores/", {
          id_caso: id_caso,
      }, function( data ) {
        
        $('#myModal').modal('toggle');
      });

    });

});





function cargar_marcadores () {
	$.get( "/archivo/cargar-marcadores/", function( data ) {
		crear_marcadores (data);
	});
}


function casos_mostrados(cantidad){
	$("#cantidad-casos").html(cantidad);	
}


function tamanio_mapa (){
	var ancho = $("#mapa").closest(".col-lg-9").width();
	$("#mapa").width(ancho+"px");
	//console.log(ancho);

	var alto = $("#mapa").closest(".container").height();
	$("#mapa").height(alto-50+"px");
	//console.log(alto);
}





