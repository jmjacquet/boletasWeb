# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from model_mommy import mommy
from django.test import Client
from tadese.forms import LiqDreiBoletaForm,LiqDreiRectifForm
from tadese.models import DriBoleta
from tadese.utilidades import ADICIONALES,hoy
from django.forms import model_to_dict
from datetime import datetime,date
from dateutil.relativedelta import *

vencido = date(1900,1,1)
no_vencido = date(3000,1,1)

class LiqDreiBoletaFormTest(TestCase):

    def setUp(self):
        # boleta = mommy.make(DriBoleta) 
        # cuota = mommy.make(DriBoleta,total=1000,derecho_neto=0,tasa_salud_publ=0) 
        self.data = {'id_padron': 123,'anio': 2020,'mes': '4','vencimiento': no_vencido,'total':100,'recargo':0,\
        'derecho_neto':0,'tasa_salud_publ':0,'retenciones':0,'adic_monto':0,'id_cuota':123456,'minimo_global':100}           
    
    def test_clean(self):        
        form = LiqDreiBoletaForm(self.data)        
        self.assertTrue (form.is_valid())        
    
    def test_clean_total(self):
        self.data.update(total=-1)
        form = LiqDreiBoletaForm(self.data)    
        self.assertFalse(form.is_valid())
    
    def test_clean_derecho_neto(self):
        self.data.update(derecho_neto=-1)
        form = LiqDreiBoletaForm(self.data)    
        self.assertFalse(form.is_valid())
    
    def test_clean_tasa_salud_publ(self):        
        self.data.update(tasa_salud_publ=-1)        
        form = LiqDreiBoletaForm(self.data)    
        self.assertFalse(form.is_valid())

class LiqDreiRectifFormTest(TestCase):

    def setUp(self):
        # boleta = mommy.make(DriBoleta) 
        # cuota = mommy.make(DriBoleta,total=1000,derecho_neto=0,tasa_salud_publ=0) 
        self.data = {'id_padron': 123,'anio': 2020,'mes': '4','vencimiento': no_vencido,'total':100,'recargo':0,\
        'derecho_neto':0,'tasa_salud_publ':0,'retenciones':0,'adic_monto':0,'id_cuota':123456,'minimo_global':100,'pago_anterior':0}           
    
    def test_clean(self):        
        form = LiqDreiRectifForm(self.data)    
        self.assertFalse(form.is_valid())
    
    def test_clean_pago_anterior(self):
        self.data.update(pago_anterior=1)
        form = LiqDreiRectifForm(self.data)    
        self.assertTrue(form.is_valid())
    