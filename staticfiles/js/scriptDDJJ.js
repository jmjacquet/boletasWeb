$(document).ready(function(){           


function CalcularTotal(){
     var subTotal = 0;
     var totImponible = 0;
     var totImp = 0;
     var totAdic = 0;
     var totalTotal = 0;
    
    $(".form-actividades tr[class='fila']").each(function(j) {

            var base = parseFloat($("input[name='periodos-"+j+"-base']").val());
            if (base == '') base=0;
            var alicuota = parseFloat($("input[name='periodos-"+j+"-alicuota']").val());
            if (alicuota == '') alicuota=0;
            var minimo = parseFloat($("input[name='periodos-"+j+"-minimo']").val());
            if (minimo == '') minimo=0; 

            var adic = parseFloat($("input[name='periodos-"+j+"-adicionales']").val());    

            var aloc_coef = parseFloat($("input[name='alicuota_coeficiente']").val());
           
            var total = parseFloat(base * alicuota/aloc_coef);
            
            
            var total2 = 0;
            
            if(total <= minimo){                        
                total2 = minimo + adic;
            }else{              
                total2 = total + adic;
            };
            
    
            $("input[name='totalActiv_"+j+"']").val(total2);  
            subTotal += parseFloat($("input[name='totalActiv_"+j+"']").val());
            totImponible += parseFloat($("input[name='periodos-"+j+"-base']").val());
            totAdic += parseFloat($("input[name='periodos-"+j+"-adicionales']").val());
            totImp += parseFloat($("input[name='periodos-"+j+"-impuesto']").val());
            
                     
        });       
        
    
    $('.Subtotal').text(subTotal);
     $("input[id='id_total_imponible']").val(totImponible);  
     $("input[id='id_total_impuestos']").val(totImp);  
     $("input[id='id_total_adicionales']").val(totAdic);  

    totalTotal = subTotal;

    $('.totalFinal').text(totalTotal);
                 
};


$('.form-actividades tr').each(function(j) {
    $("input").change(function(){
    CalcularTotal();      
     });
});

CalcularTotal();  
    
});
