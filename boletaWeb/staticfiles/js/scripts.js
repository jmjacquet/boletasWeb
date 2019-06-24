$(document).ready(function(){           

alertify.defaults.transition = "slide";
alertify.defaults.theme.ok = "btn btn-primary";
alertify.defaults.theme.cancel = "btn btn-danger";
alertify.defaults.theme.input = "form-control";

function calcular(){        
        $('.form-actividades tr').each(function(j) {
            var $base = parseFloat($("input[name='actividades-"+j+"-base']").val())|| 0;
            if ($base == '') $base=0;
            var $alicuota = parseFloat($("input[name='actividades-"+j+"-alicuota']").val())|| 0;
            if ($alicuota == '') $alicuota=0;
            var $minimo = parseFloat($("input[name='actividades-"+j+"-minimo']").val())|| 0;
            if ($minimo == '') $minimo=0; 
            var $aloc_coef = parseFloat($("input[name='alicuota_coeficiente']").val().replace(/,/, '.'))|| 0;            
            var $total = parseFloat($base * $alicuota/$aloc_coef);
            $total = $total.toFixed(2)

            if($total <= $minimo){        
                $(".totalActiv_"+j).text($minimo);
                $("input[name='actividades-"+j+"-impuesto']").val($minimo);
                
            }else{
                $(".totalActiv_"+j).text($total);
                $("input[name='actividades-"+j+"-impuesto']").val($total);          
            }      
        });       
        return false;
    };

function muestra(){
    //Función para mostrar el div que contiene la imagen Loading    
    $('#divCargando').show();
}
 
function oculta(){
    //Función para ocultar el div que contiene la imagen Loading
    $('#divCargando').hide();
}

function CalcularTotal(){
      
    var $subTotal = 0.0;
    var $totalTotal = 0.0;
    calcular();
    var $minimoBol = parseFloat($("input[name='minimo_global']").val().replace(/,/, '.'));
    $('.form-actividades tr').each(function(j) {
        $subTotal += parseFloat($(".totalActiv_"+j).text()) ;
    });    
    var $totalTotal = 0.0;    
    //Calculo el valor de los punitorios de la cuota
    var $cuota = $("input[name='id_cuota']").val();    
    muestra();
    $("#guardar").addClass("disabled");
    $("#guardar").val("Confirmar");
    $.ajax({
        url: "/punitorios/"+$cuota+"/",
        type: "get", // or "get"       
        success: function(data) {
            var $porc = parseFloat(data).toFixed(3);
            var $rec = 0;
            var $subtot2 = 0;
            
            if ($subTotal < $minimoBol){ $subTotal=$minimoBol;};
            var $subtot = parseFloat($subTotal);
            
            $('.Subtotal').text(parseFloat($subTotal).toFixed(2) );
            
            var $pago_anterior = parseFloat($("input[name='pago_anterior']").val())|| 0;
            console.log($pago_anterior);                       
            if ($pago_anterior == '') $pago_anterior=0; 
            $("input[name='pago_anterior']").val($pago_anterior);

            var $derecho_neto = parseFloat($("input[name='derecho_neto']").val())|| 0;
            if ($derecho_neto == '') $derecho_neto=0; 
            $("input[name='derecho_neto']").val($derecho_neto);                
            
            var $tasa_salud_publ = parseFloat($("input[name='tasa_salud_publ']").val())|| 0;
            if ($tasa_salud_publ == '') $tasa_salud_publ=0;                           
            $("input[name='tasa_salud_publ']").val($tasa_salud_publ);        
            
            var $adic_monto = parseFloat($("input[name='adic_monto']").val())|| 0;
            if ($adic_monto == '') $adic_monto=0;             
            $("input[name='adic_monto']").val($adic_monto);           
            
            var $retenciones = parseFloat($("input[name='retenciones']").val())|| 0;
            if ($retenciones=='') $retenciones=0;                           
            $("input[name='retenciones']").val($retenciones);                

            $subtot2 = $subtot + $derecho_neto+$tasa_salud_publ+$adic_monto+$retenciones - $pago_anterior;                        
            $rec = $subtot2 * $porc;
            $rec = parseFloat($rec).toFixed(2);
            $("input[name='recargo']").val($rec);

            var $recargo = parseFloat($("input[name='recargo']").val())|| 0;          
            if ($recargo == '') $recargo=0;                   
            $("input[name='recargo']").val($recargo);

            $totalTotal = $subtot2+$recargo;

            $('.totalFinal').text(parseFloat($totalTotal).toFixed(2)  );
            $("input[id='id_total']").val(parseFloat($(".totalFinal").text()).toFixed(2));
            $("#guardar").val("Guardar");
            $("#guardar").removeClass("disabled");
            oculta();
                }});
};

$("select[name='adic_select']").change(function(){    
    var $porc = parseFloat($("select[name='adic_select']").val())/100;
    var $subtot = parseFloat($('.Subtotal').text());
    var $tot = ($porc*$subtot).toFixed(2);
    $("input[name='adic_monto']").val($tot);
    $("input[name='adic_detalle']").val($(this).find("option:selected").text());
    CalcularTotal();  
    });

$('.form-actividades tr').each(function(j) {
    $("input").change(function(){
    CalcularTotal();      
     });
});

function deshabilitar() {
  $("#guardar").val("Confirmar");  
  $("#guardar").addClass("disabled");
};

function habilitar() {
  $("#guardar").val("Guardar");  
  $("#guardar").removeClass("disabled");
};


var inputs = document.getElementsByTagName('input');

for (i = 0; i < inputs.length; i++) {  
  inputs[i].addEventListener('input', deshabilitar, true);
};


$("#recalcular").click(function(){
    CalcularTotal();    
     });


$("#guardar").click(function(){
   $totalTotal = $("#id_total").val();       
   if ($totalTotal < 0){
        alertify.alert('ATENCIÓN','El Total a pagar no debe ser menor a $0.00!');    
    }else
    {
        $(this).attr('disabled','disabled');          
        $("#formularioDREI").submit();      
    }
    });

CalcularTotal(); 
oculta();  
});

