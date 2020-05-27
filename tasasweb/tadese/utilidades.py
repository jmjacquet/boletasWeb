# -*- coding: utf-8 -*-
from datetime import datetime, timedelta,date
from dateutil.relativedelta import *
import decimal
from django.contrib import messages
from django.conf import settings
from django.contrib.messages import constants as message_constants
import datetime

# URL_CAJERO24 = 'http://testpagos.cajero24.com/Pagos/Procesar'
URL_CAJERO24 = 'http://pagos.cajero24.com/pagos/procesar'


ANIOS = (
    ('2027', '2027'),
    ('2026', '2026'),
    ('2025', '2025'),
    ('2024', '2024'),
    ('2023', '2023'),
    ('2022', '2022'),
    ('2021', '2021'),
    ('2020', '2020'),
    ('2019', '2019'),
	('2018', '2018'),
    ('2017', '2017'),
    ('2016', '2016'),
    ('2015', '2015'),
    ('2014', '2014'),
    ('2013', '2013'),
    ('2012', '2012'),
    ('2011', '2011'),
    ('2010', '2010'),
)

TRIBUTOS_LOGIN = (
    ('1', 'TGI Urbano'),
    ('2', 'TGI Rural'),
    ('3', 'TGI SubUrbano'),
    ('5', u'Contribución de Mejoras'),
    ('6', 'DReI'),
    ('7', 'Servicios'),
    ('10', 'Convenio'),    
)

MESES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)

PERIODOS = (
    ('0', 'Todos'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)

ESTADOS = (
    (0, 'NORMAL'),
    (1, 'CONVENIO'),
    (100, 'JUDICIAL'),
    (1000, 'PAGO PENDIENTE'),
)

TIPOUSR = (
    (0, 'Contribuyente'),
    (1, 'Estudio Contable'),
    (2, 'Municipio'),
)

ADICIONALES = (
    ('0', 'Sin Adicional'),
    ('2', 'Adicional 2%'),
    ('5', 'Adicional 5%'),
    ('6', 'Adicional 6%'),
    ('8', 'Adicional 8%'),
    ('10', 'Adicional 10%'),
    ('12', 'Adicional 12%'),
)

def digVerificador(num):
    lista = list(num)
    pares= lista[1::2]
    impares= lista[0::2]
    
    totPares = 0
    totImpares = 0

    for i in pares:
        totPares=totPares+int(i*3)

    for i in impares:
        totImpares=totImpares+int(i)
 
    final = totImpares+totPares

    while (final > 9):
        cad=str(final)
        tot=0
        for i in cad:
            tot=tot+int(i)
        final=tot

    return final


def inicioMes():# pragma: no cover
    hoy=date.today()
    hoy = date(hoy.year,hoy.month,1)
    return hoy

def hoy():# pragma: no cover
    return date.today()    
    
def correr_vencimiento(vencimiento,vencimiento2,tributo):
    ''' Sirve para correr el vencimiento n dias si está entre la fdesde y fhasta definido en el tributo'''
    try:
        correr_venc_fdesde = tributo.correr_venc_fdesde
        if not vencimiento2:
            vencimiento2 = vencimiento
            
        if not correr_venc_fdesde:
            return [vencimiento,vencimiento2]
        
        correr_venc_fhasta = tributo.correr_venc_fhasta
        correr_venc_dias = tributo.correr_venc_dias
        if not correr_venc_fhasta:
            correr_venc_fhasta=date(3000,1,1)
        
        if not correr_venc_dias:
            correr_venc_dias = 0

        if (vencimiento >= correr_venc_fdesde)and(vencimiento <= correr_venc_fhasta):
            vencimiento = vencimiento + relativedelta(days=correr_venc_dias)               
            vencimiento2 = vencimiento2 + relativedelta(days=correr_venc_dias)
                 
        return [vencimiento,vencimiento2]
    except:
        return [vencimiento,vencimiento2]


from django.forms import Widget
from django.utils.safestring import mark_safe

class PrependWidget(Widget):# pragma: no cover
    def __init__(self, base_widget, data, *args, **kwargs):
        u"""Initialise widget and get base instance"""
        super(PrependWidget, self).__init__(*args, **kwargs)
        self.base_widget = base_widget(*args, **kwargs)
        self.data = data

    def render(self, name, value, attrs=None):
        u"""Render base widget and add bootstrap spans"""
        field = self.base_widget.render(name, value, attrs)
        return mark_safe((
            u'<div class="input-group">'
            u'    <span class="input-group-addon">%(data)s</span>%(field)s'
            u'</div>'
        ) % {'field': field, 'data': self.data})



MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}
