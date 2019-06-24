$(document).ready(function(){           
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
    $("#montoLiqCant").text(cant);
    console.log(cuotas);
}

$('#generarLiq').click(function(){    
    total = parseFloat(document.getElementById("totalLiq").value).toFixed(2);  
    console.log(total);
    if (total>0)
    {
      idp = document.getElementById("id_padron").value
      datos = []
      console.log(cuotas);
      $.ajax({
        url: "/punitoriosLiq/"+idp,
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
                'message': 'El monto de la Liquidación (punitorios al día de la fecha) es de : $ '+ $subtot ,
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
    } 
});

});
