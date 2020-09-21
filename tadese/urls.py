# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.conf import settings
import os
from views import *
from tasasweb.views import volverHome
from django.views.generic import RedirectView,TemplateView

# Uncomment the next two lines to enable the admin:

urlpatterns = [    
    url(r'^$', volverHome,name="inicio"),
    url(r'^municipio/$', verDDJJDrei,name="municipio"),
    url(r'^estudios/$', EstudiosView.as_view(),name="padrones_estudio"),
    url(r'^padrones/$', PadronesView.as_view(),name="padrones_responsable"),
    
    url(r'^cuotas/(?P<idp>[^/]+)/$', BusquedaCuotasView.as_view(),name="ver_cuotas"),
    url(r'^cuotas/(?P<idp>[^/]+)/(?P<anio>\d+)/$', BusquedaCuotasView.as_view(),name="buscarCuotasAP"),

    url(r'^drei/(?P<idc>\d+)/$', DreiLiquidarCreateView.as_view(),name="drei_liquidarBoleta"),
    url(r'^drei2/(?P<idb>\d+)/$', DreiLiquidarUpdateView.as_view(),name="drei_reliquidarBoleta"),
    url(r'^drei3/(?P<idb>\d+)/$', DreiRectificar.as_view(),name="drei_rectificarBoleta"),
    url(r'^drei4/(?P<idc>\d+)/$', DreiRectificarNew.as_view(),name="drei_rectificarNewBoleta"),

    url(r'^drei/eliminar/(?P<idb>[^/]+)/$', EliminarBoleta,name="eliminar_boleta"),
    url(r'^drei/modif_bases/(?P<idb>\d+)/$', DreiModifBasesView.as_view(),name="drei_modif_bases"),
    
    url(r'^punitorios/(?P<idc>\d+)/(?P<valor>\d+\.\d+)/$',calcularPunitoriosForm,name="calcularPunitorios"),
    url(r'^punitoriosLiq/$',generarPunitoriosLiq,name="generarPunitoriosLiq"),

    url(r'^imprimir/(?P<idc>\d+)/$',imprimirPDF,name="imprimirPDF"),
    url(r'^imprimir/(?P<idc>\d+)/(?P<idb>\d+)/$',imprimirPDF,name="imprimirPDFBoleta"),
    url(r'^imprimirLiqWeb/(?P<id_liquidacion>\d+)/$',imprimirPDFLiqWeb,name="imprimirPDFLiqWeb"),
    
    url(r'^drei/ddjja/(?P<idp>\d+)/$', DreiDDJJAList.as_view(),name="drei_ddjja_list"),
    url(r'^drei/ddjja/(?P<idp>\d+)/(?P<anio>\d+)/$', DreiDDJJAList.as_view(),name="drei_ddjja_list"),

    url(r'^estudios/editar/(?P<pk>\d+)$', EstudiosUpdateView.as_view(), name='estudio_editar'),
    
    url(r'^liquidacion/(?P<idp>\d+)/$', generarLiquidacion,name="generarLiquidacion"),
    
    url(r'^estudios/passwd/(?P<usrEstudio>.+)$', mandarEmailEstudio, name='mandarEmailEstudio'),

    url(r'^suscripcion/alta/(?P<idp>\d+)/$', suscripcion_alta,name="suscripcion_alta"),
    url(r'^suscripcion/baja/(?P<idp>\d+)/$', suscripcion_baja,name="suscripcion_baja"),    

    url(r'^pago/$', generarPago,name="pago"),

    url(r'^pago/exito/$', generarPagoExito,name="pago_exito"),
    url(r'^pago/error/(?P<idp>\d+)/$', generarPagoError,name="pago_error"),

   
    ]