$(document).ready(function()
{           
var cuotas = [];
alertify.defaults.transition = "slide";
alertify.defaults.theme.ok = "btn btn-primary";
alertify.defaults.theme.cancel = "btn btn-danger";
alertify.defaults.theme.input = "form-control";


$("#checkall").click (function () {
     var checkedStatus = this.checked;
    $("input[class='tildado']").each(function () {
        $(this).prop("checked", checkedStatus);
        $(this).change();
     });
  });
 
  
  $("input[class='tildado']").change(function() {      
       cuotas = []
      checkBoxClick();               
  });
    
  
  function checkBoxClick() {
    
    var total = 0.00;
    var montoLiq = 0.00;    
    cant = 0; 
    $("input[class='tildado']").each(function(index,checkbox){
        if(checkbox.checked){               
         idcta = document.getElementById(checkbox.id+"_id_cuota").value               
         saldo = parseFloat(document.getElementById("saldo_"+checkbox.id).value.replace(/,/, '.'));
         montoLiq = document.getElementById("total_"+checkbox.id)       ;
         if (montoLiq) { saldo = parseFloat(montoLiq.value.replace(/,/, '.')); }         
         cuotas.push(idcta);     
         total += saldo;
         cant += 1; 
         
         $(checkbox).closest('tr').toggleClass('selected', checkbox.checked);
    }
    else {  
        if($(checkbox).closest('tr').hasClass('selected')){
          $(checkbox).closest('tr').removeClass('selected');}
        }
    });
    $("#montoLiq").text(parseFloat(total).toFixed(2));
    $("#totalLiq").val(parseFloat(total).toFixed(2));
    $("#totalLiqCant").val(parseFloat(cant).toFixed(2));
    $("#montoLiqCant").text(cant);
    
}

$('#generarLiq').click(function(){    
    total = parseFloat(document.getElementById("totalLiq").value).toFixed(2);  
    cant = parseFloat(document.getElementById("totalLiqCant").value).toFixed(2);  
    if (cant <=1){
      alertify.alert('ATENCIÓN','¡Debe seleccionar 2 o más Cuotas!');    
    }
    else{
      if (total>0)
      {
        idp = document.getElementById("id_padron").value
        datos = []
        
        $.ajax({
          url: "/punitoriosLiq/",
          type: "get",
          dataType: 'json',
          data: {'cuotas[]': cuotas},
          success: function(data) {
              var $subtot = 0;
              for(var key in data){
                $subtot += parseFloat(data[key]);};
             
              $subtot = $subtot.toFixed(2);

              var closable = alertify.dialog('confirm').setting('closable');
              //grab the dialog instance and set multiple settings at once.
              
              alerta= alertify.dialog('confirm')
                .set({
                  'labels':{ok:'Guardar e Imprimir', cancel:'Cancelar'},
                  'message': 'El monto total actualizado de la Liquidación es de : $ '+ $subtot ,
                  'onok': function(){ 
                    datos = data;
                    $.ajax({
                      url: "/liquidacion/"+idp,
                      type: "get",
                      dataType: 'json',
                      data: {'cuotas[]': cuotas},
                      success: function(data) {
                        // alertify.success('El monto a pagar es: $ '+ $subtot);
                        url = "/imprimirLiqWeb/"+data;
                        var win = window.open(url, '_blank');
                        win.focus();
                        
                        location.reload();
                          }});                  
                  },
                  'oncancel': function(){ location.reload();}
                });
                alerta.setHeader('Liquidación OnLine');
                alerta.show();
          }});
      }else{
           alertify.alert('ATENCIÓN','¡Debe seleccionar alguna Cuota!');    
        }
    }
});

$('#suscribir').click(function(){    
     idp = document.getElementById("id_padron").value;
     var closable = alertify.dialog('confirm').setting('closable');      
     alerta= alertify.dialog('confirm')
        .set({
          'labels':{ok:'Aceptar', cancel:'Cancelar'},
          'message': '¿Desea suscribirse a Boleta Digital?',
          'onok': function(){ 
                url = "/suscripcion/alta/"+idp;
                window.location.href = url;                
          },
          'oncancel': function(){ location.reload();}
        });
        alerta.setHeader('Suscripción Boleta OnLine');
        alerta.show();
});

$('#desuscribir').click(function(){    
     idp = document.getElementById("id_padron").value;
     var closable = alertify.dialog('confirm').setting('closable');      
     alerta= alertify.dialog('confirm')
        .set({
          'labels':{ok:'Aceptar', cancel:'Cancelar'},
          'message': '¿Desea desuscribirse a Boleta Digital?' ,
          'onok': function(){ 
                url = "/suscripcion/baja/"+idp;
                window.location.href = url;
          },
          'oncancel': function(){ location.reload();}
        });
        alerta.setHeader('Desuscripción Boleta OnLine');
        alerta.show();
});

$('#formPagos').on('submit', function(evt) {
          
          // setTimeout(function() {
          //      window.location.reload();
          // },500);
          // this.submit();
    });

  $('#generarPago').click(function(){    
    total = parseFloat(document.getElementById("totalLiq").value).toFixed(2);      
    if (total>0)
    {
      // idp = document.getElementById("id_padron").value
      datos = []
      
      $.ajax({
        url: "/punitoriosLiq/",
        type: "get",
        dataType: 'json',
        data: {'cuotas[]': cuotas},
        success: function(data) {
            var $subtot = 0;
            for(var key in data){
              $subtot += parseFloat(data[key]);};
           
            $subtot = $subtot.toFixed(2);

            var closable = alertify.dialog('confirm').setting('closable');
            alerta= alertify.dialog('confirm')
              .set({
                'labels':{ok:'Pagar', cancel:'Cancelar'},
                'message': 'El monto total actualizado a pagar es de : $ '+ $subtot +'<br>(recuerde que el proceso de acreditación puede demorar hasta 48hs hábiles).' ,
                'onok': function(){ 
                  datos = data;
                  $.ajax({
                    url: "/pago/",
                    type: "get",
                    dataType: 'json',
                    data: {'cuotas[]': cuotas},
                    success: function(data) {
                      
                      var form = $('#formPagos');
                      var urlExito = data[0];
                      $.each(data[1], function (i, v) {                          
                           $("<input>").attr({
                                'type':'hidden',
                                'name':v[0][0],
                            }).val(v[0][1]).appendTo(form);
                      });                      
                      var exito= document.getElementsByName("UrlExito")[0];
                      exito.value=urlExito;

                      var NoComercio = data[2];
                      var codigo= document.getElementsByName("NoComercio")[0];
                      codigo.value=NoComercio;    
                      
                      form.submit();
                      location.reload();

                      },
                    error: function(message) {                 
                        console.log(message);
                    },
                  });                  
                },
                'oncancel': function(){ location.reload();}
              });
              alerta.setHeader('Pago de Cuotas OnLine');
              alerta.show();
                },
        error: function(message) {                 
            console.log(message);
        },
      });
    } 
    else{
         alertify.alert('ATENCIÓN','¡Debe seleccionar alguna Cuota!');    
      }
});

});
