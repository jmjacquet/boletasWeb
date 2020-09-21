# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from model_mommy import mommy
from django.test import TestCase
from tadese.models import Tributo,TributoInteres,Cuotas,DriBoleta,DriEstudio,DriCuotaActividad,DriBoleta_actividades,Suscriptores
from datetime import datetime,date
from dateutil.relativedelta import *
from tadese.utilidades import ESTADOS,hoy

vencido = date(1900,1,1)
no_vencido = date(3000,1,1)

class TributoTest(TestCase):
	def test_unicode(self):
		un_tributo = mommy.make(Tributo,descripcion='TGI')      
		self.assertTrue(isinstance(un_tributo, Tributo))             
		self.assertEqual(un_tributo.__unicode__(), un_tributo.descripcion)

	def test_get_abreviatura(self):
		un_tributo = mommy.make(Tributo,abreviatura='TGIU')
		self.assertTrue(isinstance(un_tributo, Tributo))             
		self.assertEqual(un_tributo.get_abreviatura, un_tributo.abreviatura)


class TributoInteresTest(TestCase):
	def test_unicode(self):
		un_tributo_i = mommy.make(TributoInteres,id_tributo=1,interes=0)      
		self.assertTrue(isinstance(un_tributo_i, TributoInteres)) 
		descr = u'%s - %s' % (un_tributo_i.id_tributo,un_tributo_i.interes)            
		self.assertEqual(un_tributo_i.__unicode__(), descr)

class DriEstudioTest(TestCase):
	def test_unicode(self):
		estudio = mommy.make(DriEstudio)      
		self.assertTrue(isinstance(estudio, DriEstudio)) 
		descr = u'%s - %s' % (estudio.numero, estudio.denominacion)
		self.assertEqual(estudio.__unicode__(), descr)

class CuotasTest(TestCase):        
	def setUp(self):
		self.vencido=vencido
		self.hoy = hoy()
		self.un_tributo = mommy.make(Tributo,descripcion='TGI',abreviatura='TGIU')      
		self.cuota = mommy.make(Cuotas,tributo=self.un_tributo,vencimiento=self.hoy,estado=0)      
		self.cuota_pagada = mommy.make(Cuotas,tributo=self.un_tributo,saldo=0)		
		self.cuota_vencida = mommy.make(Cuotas,tributo=self.un_tributo,saldo=1,vencimiento=self.vencido,estado=0)

	def test_unicode(self):
		self.assertTrue(isinstance(self.cuota, Cuotas))
		descr = u'%s --> %s' % (self.cuota.padron, self.cuota.id_padron)        
		self.assertEqual(self.cuota.__unicode__(), descr)

	def test_get_datos(self):
		descr = u'%s/%s-%s(%s)' % (self.cuota.cuota,self.cuota.anio,self.cuota.padron, self.cuota.tributo.abreviatura)
		self.assertEqual(self.cuota.get_datos(), descr)    

	def test_get_estado_VENCIDO(self):
		descr='VENCIDO'
		self.assertEqual(self.cuota_vencida.get_estado, descr)

	def test_get_estado_PAGADO(self):
		descr='PAGADO'		
		self.assertEqual(self.cuota_pagada.get_estado, descr)

	def test_get_estado_OTROS(self):		
		self.assertEqual(self.cuota.get_estado, ESTADOS[self.cuota.estado][1])

	def test_get_responsable(self):
		descr = u'%s (%s)' % (self.cuota.nombre,self.cuota.nrodocu)
		self.assertEqual(self.cuota.get_responsable(), descr)

	# def test_get_boletas(self):
	# 	boletas = mommy.make( DriBoleta,id_cuota=self.cuota,_quantity=3) 
	# 	boleta = mommy.make( DriBoleta,_quantity=2) 		
	# 	self.assertEqual(list(self.cuota.get_boletas()), boletas)
	# 	self.assertNotEqual(list(self.cuota.get_boletas()), boleta)

	# def test_get_boletas_null(self):
	# 	try:
	# 		boletas = mommy.make( DriBoleta,id_cuota=self.cuota,_quantity=3) 
	# 	except:
	# 		boletas = None
	# 	self.assertEqual(list(self.cuota.get_boletas()), boletas)		


	def test_get_boleta_venc(self):
		boleta_venc = mommy.make( DriBoleta,id_cuota=self.cuota,fechapago=self.vencido) 
		self.assertTrue(self.cuota.get_boleta_venc)
		boleta = mommy.make( DriBoleta,id_cuota=self.cuota,fechapago=self.hoy) 
		self.assertFalse(self.cuota.get_boleta_venc)		
		

class DriCuotaActividadTest(TestCase):
	def test_unicode(self):
		cuota_activ = mommy.make(DriCuotaActividad)      		
		cuota_activp = mommy.make(DriCuotaActividad,actividad_principal='S')      		
		detalle = u'%s - %s' % (cuota_activ.codigo,cuota_activ.denominacion)
		detallep = u'(*) %s - %s' % (cuota_activp.codigo,cuota_activp.denominacion)  
		self.assertEqual(cuota_activ.__unicode__()[:200], detalle)
		self.assertNotEqual(cuota_activ.__unicode__()[:200], detallep)
		self.assertEqual(cuota_activp.__unicode__()[:200], detallep)
		self.assertNotEqual(cuota_activp.__unicode__()[:200], detalle)

	def test_get_actividad(self):
		cuota_activ = mommy.make(DriCuotaActividad)      		
		cuota_activp = mommy.make(DriCuotaActividad,actividad_principal='S')      		
		detalle = u'%s - %s' % (cuota_activ.codigo,cuota_activ.denominacion)
		detallep = u'(*) %s - %s' % (cuota_activp.codigo,cuota_activp.denominacion)  
		self.assertEqual(cuota_activ.get_actividad()[:200], detalle)
		self.assertNotEqual(cuota_activ.get_actividad()[:200], detallep)
		self.assertEqual(cuota_activp.get_actividad()[:200], detallep)
		self.assertNotEqual(cuota_activp.get_actividad()[:200], detalle)
	   
class DriBoletaTest(TestCase):
	def test_unicode(self):
		boleta = mommy.make(DriBoleta,fechapago=vencido)       
		descr = u'%s %s %s' % (boleta.id_padron,boleta.anio,boleta.mes)       
		self.assertEqual(boleta.__unicode__(), descr)
	
class DriBoleta_actividadesTest(TestCase):
	def test_unicode(self):
		boleta = mommy.make(DriBoleta_actividades)       
		descr = u'%s' % (boleta.activ_descr)      
		self.assertEqual(boleta.__unicode__(), descr)

class SuscriptoresTest(TestCase):
	def test_unicode(self):
		suscr = mommy.make(Suscriptores)
		descr = u'%s' % (suscr.id)    
		self.assertEqual(suscr.__unicode__(), descr)

	def test_activa(self):
		suscr_baja = mommy.make(Suscriptores,fecha_baja=vencido)       
		suscr1 = mommy.make(Suscriptores)       
		suscr2 = mommy.make(Suscriptores,fecha_baja=hoy())
		suscr3 = mommy.make(Suscriptores,fecha_baja=no_vencido)       
		self.assertTrue(suscr1.activa)
		self.assertFalse(suscr2.activa)
		self.assertTrue(suscr3.activa)
		self.assertFalse(suscr_baja.activa)



