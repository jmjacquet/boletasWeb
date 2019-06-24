# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.conf import settings
import os
from views import *
from django.views.generic import RedirectView,TemplateView
import signals
# Uncomment the next two lines to enable the admin:


urlpatterns = patterns('tadese.views',
	
    url(r'^municipio/$', verDDJJDrei,name="municipio"),
    url(r'^estudios/$', EstudiosView.as_view(),name="padrones_estudio"),
    url(r'^padrones/$', ResponsablesView.as_view(),name="padrones_responsable"),
    
    url(r'^cuotas/(?P<idp>[^/]+)/$', BusquedaCuotasView.as_view(),name="ver_cuotas"),
    url(r'^cuotas/(?P<idp>[^/]+)/(?P<anio>\d+)/$', BusquedaCuotasView.as_view(),name="buscarCuotasAP"),


    url(r'^drei/(?P<idc>\d+)/$', DreiLiquidarCreateView.as_view(),name="drei_liquidarBoleta"),
    url(r'^drei2/(?P<idb>\d+)/$', DreiLiquidarUpdateView.as_view(),name="drei_reliquidarBoleta"),
    url(r'^drei3/(?P<idb>\d+)/$', DreiRectificar.as_view(),name="drei_rectificarBoleta"),
    url(r'^drei4/(?P<idc>\d+)/$', DreiRectificarNew.as_view(),name="drei_rectificarNewBoleta"),

    url(r'^drei/eliminar/(?P<idb>[^/]+)/$', EliminarBoleta,name="eliminar_boleta"),

    url(r'^drei/verificarCuota/(?P<idc>\d+)/$', verificarCuota,name="drei_verificarCuota"),

    url(r'^punitorios/(?P<idc>\d+)/$',calcularPunitoriosForm,name="calcularPunitorios"),
    url(r'^punitoriosLiq/(?P<idp>\d+)/$',generarPunitoriosLiq,name="generarPunitoriosLiq"),

    url(r'^imprimir/(?P<idc>\d+)/$',imprimirPDF,name="imprimirPDF"),
    url(r'^imprimir/(?P<idc>\d+)/(?P<idb>\d+)/$',imprimirPDF,name="imprimirPDFBoleta"),
    url(r'^imprimirLiqWeb/(?P<id_liquidacion>\d+)/$',imprimirPDFLiqWeb,name="imprimirPDFLiqWeb"),

    url(r'^boletaTGI/$', TemplateView.as_view(template_name="boletas/boleta_tasas.html")),
    url(r'^boletaDREI/$', TemplateView.as_view(template_name="boletas/boleta_drei.html")),
    
    url(r'^drei/ddjja/(?P<idp>\d+)/$', DreiDDJJAList.as_view(),name="drei_ddjja_list"),
    url(r'^drei/ddjja/(?P<idp>\d+)/(?P<anio>\d+)/$', DreiDDJJAList.as_view(),name="drei_ddjja_list"),

    url(r'^estudios/editar/(?P<pk>\d+)$', EstudiosUpdateView.as_view(), name='estudio_editar'),

    url(r'^liquidacion/(?P<idp>\d+)/$', generarLiquidacion,name="generarLiquidacion"),

    url(r'^estudios/passwd/(?P<usrEstudio>.+)$', mandarEmailEstudio, name='mandarEmailEstudio'),
    
    )