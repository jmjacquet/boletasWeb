$(document).ready(function()
{           

alertify.defaults.transition = "slide";
alertify.defaults.theme.ok = "btn btn-primary";
alertify.defaults.theme.cancel = "btn btn-danger";
alertify.defaults.theme.input = "form-control";


$("input[type=number]").click(function() {
    this.select()
});


function calcularActiv(j){                
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
        };
        

        return true;
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
    var $minimoBol = parseFloat($("input[name='minimo_global']").val().replace(/,/, '.'));
    
    $('.form-actividades tr').each(function(j) {        
        $subTotal += parseFloat($("input[name='actividades-"+j+"-impuesto']").val())|| 0 ;
    });    
    
    var $totalTotal = 0.0;    
    //Calculo el valor de los punitorios de la cuota
    var $cuota = $("input[name='id_cuota']").val();    
    if ($subTotal < $minimoBol){ $subTotal=$minimoBol;};
    
    var $subtot = parseFloat($subTotal);
    var $rec = 0;
    var $subtot2 = 0;
    
    $('.Subtotal').text(parseFloat($subTotal).toFixed(2) );
    
    var $pago_anterior = parseFloat($("input[name='pago_anterior']").val())|| 0;            
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
    $subtot2 =parseFloat($subtot2);
    
    muestra();
    $("#guardar").addClass("disabled");
    $("#guardar").val("Confirmar");
    $.ajax({
        url: "/punitorios/"+$cuota+"/"+($subtot2).toFixed(2),
        type: "get", // or "get"       
        // async: false,
        success: function(data) {            
            $rec = parseFloat(data);
            $("input[name='recargo']").val($rec);
            var $recargo = parseFloat($("input[name='recargo']").val())|| 0;                   
            $("input[name='recargo']").val($recargo);
            $totalTotal = $subtot2 + $recargo;
            
            $('.totalFinal').text(parseFloat($totalTotal).toFixed(2)  );
            $("input[id='id_total']").val(parseFloat($(".totalFinal").text()).toFixed(2));            
            
            $("#guardar").val("Guardar");
            $("#guardar").removeClass("disabled");
            oculta();
            },
        error : function(message) {                 
            console.log(message);
            $("#guardar").val("Guardar");
            $("#guardar").removeClass("disabled");
            oculta();
            }
        });    
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
        $("input[name='actividades-"+j+"-base']").change(function(){
            calcularActiv(j);
            CalcularTotal()
         });
        $("input[name='actividades-"+j+"-alicuota']").change(function(){
            calcularActiv(j);
            CalcularTotal()
         });
        $("input[name='actividades-"+j+"-minimo']").change(function(){
            calcularActiv(j);
            CalcularTotal()
         });
});

$('.form-adicionales tr').each(function(j) {        
        $("input").change(function(){            
            CalcularTotal()
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


$("#guardar").click(function(){
   CalcularTotal();
   $totalTotal = $("#id_total").val();       
   if ($totalTotal < 0){
        alertify.alert('ATENCIÓN','El Total a pagar no debe ser menor a $0.00!');    
    }else
    {
        
        $(this).attr('disabled','disabled');          
        $("#formularioDREI").submit();      
    }
    });

function recalcular(){
  $('.form-actividades tr').each(function(j) { 
    calcularActiv(j);
    });
    CalcularTotal();
}
recalcular(); 
oculta();  
});

