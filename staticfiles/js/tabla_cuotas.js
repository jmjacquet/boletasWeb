$(document).ready(function() { 

moment.locale('es');
$.fn.dataTable.moment('DD/MM/YYYY'); 
var tabla = $('#tablaCuotas').DataTable({
            "language": {
                "decimal": ",",
                "thousands": ".",                
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "No hay registros en esta tabla",
                "sInfo": " _TOTAL_ cuotas encontradas.",
                "sInfoEmpty": "No existen cuotas para el período seleccionado",
                "sInfoFiltered": "(de un total de _MAX_ cuotas)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ".",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "Primero",
                    "sLast": "Último",
                    "sNext": "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                },
                      
            },                      
            "columnDefs": [ {
                  "targets"  : 'no-sort',
                  "orderable": false,
                }],          
           "scrollY":        '65vh',
           "scrollCollapse": false,
           "paging":   false,
           "lengthMenu": [[20, 50, -1], [20, 50, "Todos"]],
           "autoWidth": true,           
           "order": [],
           "colReorder": true,
           "searching": true,
            "responsive": true,
            // dom: 'frtlip',
            // "dom": '<"top"i>rt<"pie"lp><"clear">',
             // "dom": '<"datatable_top"lf<t>"pie"ip>',
            "dom": "<'col-sm-12' <'row fondo_busqueda'<'col-xs-4 col-sm-3'f><'col-xs-8 col-sm-9'i>><'row'<tr>>>",
           
         
    
            initComplete: function () {
               // this.api().columns().every( function () {[0, 1, 9]
                this.api().columns([1,2,3]).every( function () {
                    var column = this;
                    var select = $('<select class="form-control"><option value="">Todos</option></select>')
                        .appendTo( $(column.footer()).empty() )
                        .on( 'change', function () {
                            var val = $.fn.dataTable.util.escapeRegex(
                                $(this).val()
                            );
     
                            column
                                .search( val ? '^'+val+'$' : '', true, false )
                                .draw();
                        } );
     
                     column.data().unique().sort().each( function ( d, j ) {
                    //column.cells('', column[0]).render('display').sort().unique().each( function ( d, j ){
                     select.append( '<option value="'+d+'">'+d+'</option>' )
                    } );
                } );

            },
            footerCallback: function ( row, data, start, end, display ) {
            var api = this.api(), data;
            var floatVal = function (i) {
                if (typeof i === "number") {
                    return i;
                } else if (typeof i === "string") {
                    i = i.replace(/\$/g, "");
                    i = i.replace(/\,/g ,"");                    
                    i = i.replace(/\./g, "");                    
                    var result = parseFloat(i)/100;
                    
                    if (isNaN(result)) {
                        try {
                            var result = $jq(i).text();
                            result = parseFloat(result);
                            if (isNaN(result)) { result = 0 };
                            return result * 1;
                        } catch (error) {
                            return 0;
                        }
                    } else {
                        return result * 1;
                    }
                } else {
                    alert("Unhandled type for totals [" + (typeof i) + "]");
                    return 0
                }
            };
                        
            
            pageTotal = api.column(7, { page: 'current'} ).data().reduce( function (a, b) {return floatVal(a) + floatVal(b);}, 0 );            
            $( api.column(7).footer() ).html('$'+pageTotal.toLocaleString(undefined,{minimumFractionDigits:2}));
            
        }
        });

       

});
