# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase,RequestFactory
from model_mommy import mommy
from tadese.views import padrones_x_estudio,padrones_x_responsable,cuotas_x_padron,puedeVerPadron,VariablesMixin,getVariablesMixin
from tadese.views import generarCodBar,get_suscriptor
from tadese.models import DriEstudio,DriEstudioPadron,Tributo,Cuotas,DriBoleta,TributoInteres
from tadese.models import Configuracion,UserProfile,Suscriptores
from tadese.punitorios import punitorios
from django.test.client import Client
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tadese.utilidades import correr_vencimiento
from datetime import datetime,date
from django.conf import settings

hoy = date.today()

class VariablesMixinTest(TestCase):
	def setUp(self):
		self.config = mommy.make(Configuracion,id=000)		

	class VistaView(VariablesMixin, TemplateView):
		pass

	def test_variables(self):
	    vista = self.VistaView()
	    context = vista.get_context_data()
	    self.assertNotEqual(context['idMuni'],None)
	    self.assertNotEqual(context['dirMuni'],None)
	    self.assertNotEqual(context['DIR_MUNIS'],None)
	    self.assertNotEqual(context['sitio'],None)
	    sitio = context['sitio']
	    self.assertEqual(sitio.id,000)
	    self.assertNotEqual(context['puede_rectificar'],None)
	    self.assertNotEqual(context['fecha_hoy'],None)
	    self.assertNotEqual(context['pago_online'],None)
	    self.assertNotEqual(context['suscripcion'],None)	    

	def test_getVariablesMixin(self):
		self.factory = RequestFactory()
		ctx = getVariablesMixin(self.factory)		
		self.assertNotEqual(ctx,{}) 
	    

class ConsultasTest(TestCase):
	"""docstring for PadronxesxEstudioTest"""
	def setUp(self):
		self.un_tributo = mommy.make(Tributo,id_tributo=6,descripcion='DReI',abreviatura='DRI')      
		self.cuota = mommy.make(Cuotas,tributo=self.un_tributo,id_padron=1,id_responsable=1) 
		self.estudio = mommy.make(DriEstudio)
		self.padrones_estudio = mommy.make(DriEstudioPadron,id_estudioc=self.estudio,id_padron=1)
		self.cuotas = mommy.make(Cuotas,tributo=self.un_tributo,id_padron=1,id_responsable=2,_quantity=3)

	def test_padrones_estudio(self):
		"""id_estudioc"""		
		p = padrones_x_estudio(self.estudio.pk)		
		self.assertTrue(isinstance(p,list))
		self.assertEqual(len(p),1)
		p2 = padrones_x_estudio(self.estudio.pk+1)		
		self.assertTrue(isinstance(p2,list))
		self.assertEqual(len(p2),0)

	def test_padrones_x_responsable(self):
		"""idResp,idPadron=None"""				
		p = padrones_x_responsable(1,1)		
		self.assertIsNotNone(p)
		self.assertEqual(len(p),1)
		p = padrones_x_responsable(1,2)
		self.assertIsNotNone(p)
		self.assertEqual(len(p),0)
		p = padrones_x_responsable(1)
		self.assertIsNotNone(p)
		self.assertEqual(len(p),1)
		p = padrones_x_responsable(None)
		self.assertEqual(len(p),0)

	def test_cuotas_x_padron(self):
		"""idResp,IdPadron"""		
		cuotas = cuotas_x_padron(2,1)
		self.assertEqual(len(cuotas),len(self.cuotas))
		cuotas = cuotas_x_padron(None,1)
		self.assertEqual(len(cuotas),4)
		cuotas = cuotas_x_padron(2,2)
		self.assertEqual(len(cuotas),0)

from django.contrib import messages
class ContribuyentesTest(TestCase):
	def setUp(self):
		self.config = mommy.make(Configuracion,id=000)
		self.config.save()
		self.user = User.objects.create_user(username='juanma', password='qwerty')
		self.factory = RequestFactory()
		self.usprfl = UserProfile(user=self.user,id_responsable=1,tipoUsr=0)            	
		self.usprfl.save()
		self.client = Client()
		self.client.force_login(self.user)
		self.request = self.factory.get('/')
		self.request.user = self.user
		self.cuotas = mommy.make(Cuotas,id_padron=1,padron='001',id_responsable=1,_quantity=3)
		  

	def test_PadronesView(self):
		response = self.client.get(reverse('padrones_responsable'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'padrones_representante.html')

		context = response.context
		self.assertNotEqual(context['padr'],None)
		self.assertNotEqual(context['padron'],None)

		response2 = self.client.get(reverse('padrones_estudio'))
		self.assertEqual(response2.status_code, 302)

	def test_BusquedaCuotasView(self):
		response = self.client.get(reverse('ver_cuotas',kwargs={'idp':1}))
		context = response.context
		self.assertEqual(response.status_code, 200)
		self.assertNotEqual(context['padr'],None)
		self.assertNotEqual(context['cuotas'],None)

		response2 = self.client.get(reverse('ver_cuotas', kwargs={'idp': 2}))
		context = response2.context
		self.assertEqual(context['padr'],None)
		self.assertEqual(context['cuotas'],None)

	def test_EliminarBoleta(self):
		self.boleta1 = mommy.make(DriBoleta,id_boleta=1,anio=2020,mes=4,id_cuota=self.cuotas[0],id_padron=1) 
		self.boleta2 = mommy.make(DriBoleta,id_boleta=2,anio=2020,mes=3,id_cuota=self.cuotas[1],id_padron=2) 
		self.boleta3 = mommy.make(DriBoleta,id_boleta=3,anio=2020,mes=4,id_cuota=self.cuotas[0],id_padron=1) 
		boleta = DriBoleta.objects.filter(id_boleta=self.boleta1.id_boleta).first()		
		self.assertNotEqual(boleta, None)		
		#La elimina OK
		response = self.client.get(reverse('eliminar_boleta',kwargs={'idb':1}))
		msjs = [m.level for m in messages.get_messages(response.wsgi_request)]
		self.assertIn(messages.SUCCESS, msjs)		
		boleta = DriBoleta.objects.filter(id_boleta=self.boleta1.id_boleta).first()
		self.assertEqual(boleta, None)

		#NO La elimina OK
		response2 = self.client.get(reverse('eliminar_boleta',kwargs={'idb':4}))
		msjs = [m.level for m in messages.get_messages(response2.wsgi_request)]
		self.assertIn(messages.ERROR, msjs)		
		self.assertRedirects(response2, reverse('padrones_responsable'))

	
class EstudiosTest(TestCase):
	def setUp(self):
		self.config = mommy.make(Configuracion,id=000)
		self.config.save()
		self.user = User.objects.create_user(username='juanma', password='qwerty')
		self.factory = RequestFactory()
		self.usprfl = UserProfile(user=self.user,tipoUsr=1,id_estudioc=1)            	
		self.usprfl.save()
		self.client = Client()
		self.client.force_login(self.user)
		self.request = self.factory.get('/')
		self.request.user = self.user
		self.estudio = mommy.make(DriEstudio,id_estudioc=1,numero='1',denominacion='Estudio PEPE',usuario='qwerty',clave='qwerty',email='jmjacquet@gmail.com')
		un_tributo = mommy.make(Tributo,id_tributo=6,descripcion='DReI',abreviatura='DRI')      
		self.padrones_estudio = mommy.make(DriEstudioPadron,id_estudioc=self.estudio,id_padron=1)
		self.cuotas = mommy.make(Cuotas,tributo=un_tributo,id_padron=1,id_responsable=2,_quantity=3)

	def test_EstudiosView(self):
		response = self.client.get(reverse('padrones_estudio'))				
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'padrones_estudio.html')
		
		context = response.context
		self.assertNotEqual(context['estudio'],None)
		self.assertNotEqual(context['padr'],None)
		self.assertNotEqual(context['padron'],None)

		response2 = self.client.get(reverse('padrones_responsable'))		
		self.assertEqual(response2.status_code, 302)

	def test_EstudiosUpdateView(self):
		response = self.client.get(reverse('estudio_editar',kwargs={'pk':1}))				
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'estudio_update.html')
		
		context = response.context
		self.assertNotEqual(context['sitio'],None)		

		response2 = self.client.get(reverse('estudio_editar',kwargs={'pk':2}))		
		self.assertEqual(response2.status_code, 302)

		
class UtilidadesTest(TestCase):
	"""docstring for """
	def setUp(self):		
		self.un_tributo = mommy.make(Tributo,id_tributo=1,descripcion='TGIs',abreviatura='TGIU',correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=15)      
		self.otro_tributo = mommy.make(Tributo,id_tributo=2,descripcion='TGIs',abreviatura='TGIR',correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      		
		self.cuota = mommy.make(Cuotas,id_cuota=1,tributo=self.un_tributo,cuota='1',anio=2020,\
			vencimiento=date(2020,1,15),segundo_vencimiento=date(2020,2,15),id_padron=1,padron='001',id_responsable=1) 				
		self.config = mommy.make(Configuracion,id=000,longitudCodigoBarra=48)
		self.cuota2 = mommy.make(Cuotas,id_cuota=2,tributo=self.otro_tributo,cuota='1',anio=2020,\
			vencimiento=date(2020,1,15),segundo_vencimiento=date(2020,2,15),id_padron=2,padron='001',id_responsable=1) 

	def test_generarCodBar(self):
		"""generarCodBar(idc,total1,total2,vencimiento,vencimiento2)"""				
		p = generarCodBar(None,1,1,None,None)				
		self.assertEqual(p,None)		
		p = generarCodBar(1,1,None,None,None)		
		self.assertEqual(p,None)
		p = generarCodBar(1,None,None,None,None)		
		self.assertEqual(p,None)

		cb = generarCodBar(1,100,100,None,None)		
		self.assertNotEqual(cb,None)		
		self.assertEqual(len(cb),48)		
		self.assertNotEqual(len(cb),60)		

		cod = generarCodBar(1,100,100000,None,None)
		self.assertEqual(len(cod),60)		

	def test_correr_vencimiento(self):
		"""correr_vencimiento(vencimiento,vencimiento2,tributo)"""
		v1 = correr_vencimiento(self.cuota.vencimiento,self.cuota.segundo_vencimiento,self.un_tributo)
		self.assertTrue(v1[0])
		self.assertTrue(v1[1])
		self.assertTrue(v1[0]>self.cuota.vencimiento)
		v2 = correr_vencimiento(self.cuota2.vencimiento,self.cuota2.segundo_vencimiento,self.otro_tributo)
		self.assertTrue(v2[0]==self.cuota2.vencimiento)
		v3 = correr_vencimiento(self.cuota.vencimiento,None,self.un_tributo)				
		self.assertTrue(v3[0])
		self.assertTrue(v3[1])
		self.assertTrue(v3[1]==v3[0])

from django.core import mail		
class MandarEmailTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		# Set up data for the whole TestCase
		cls.config = mommy.make(Configuracion,id=000)
		cls.config.save()
		cls.user = User.objects.create_user(username='qwerty', password='qwerty')
		cls.factory = RequestFactory()
		cls.usprfl = UserProfile(user=cls.user,id_responsable=1,tipoUsr=0)            	
		cls.usprfl.save()
		cls.client = Client()
		cls.client.force_login(cls.user)
		cls.request = cls.factory.get('/')
		cls.request.user = cls.user
		cls.estudio = mommy.make(DriEstudio,id_estudioc=1,usuario='qwerty',clave='qwerty',email='jmjacquet@gmail.com')
				

	def test_solo_ajax(self):
		"""
		Mandar email a estudios_contables con la password
		"""        
		response = self.client.get(reverse('mandarEmailEstudio',kwargs={'usrEstudio':'qwerty'}))		
		self.assertEqual(response.status_code,200)
		message=(u"ERROR sólo AJAX").encode('utf-8')		
		self.assertEqual(response.content,message)		
		self.assertEqual(len(mail.outbox),0)

	def test_mail_enviado(self):
		"""
		Mandar email a estudios_contables con la password
		"""        
		response = self.client.get(reverse('mandarEmailEstudio',kwargs={'usrEstudio':'qwerty'}),HTTP_X_REQUESTED_WITH='XMLHttpRequest')		
		self.assertEqual(response.status_code,200)
		message=(u"¡El e-mail fué enviado con éxito!").encode('utf-8')						
		self.assertEqual(len(mail.outbox),1)

	def test_error_usuario(self):
		"""
		Mandar email a estudios_contables con la password
		"""        
		response = self.client.get(reverse('mandarEmailEstudio',kwargs={'usrEstudio':'papapapa'}),HTTP_X_REQUESTED_WITH='XMLHttpRequest')				
		self.assertEqual(len(mail.outbox),0)		

	def test_error_destinatario(self):
		"""
		Mandar email a estudios_contables con la password
		""" 
		self.estudio = mommy.make(DriEstudio,id_estudioc=1,usuario='qwerty',clave='qwerty',email=None)
		response = self.client.get(reverse('mandarEmailEstudio',kwargs={'usrEstudio':'qwerty'}),HTTP_X_REQUESTED_WITH='XMLHttpRequest')				
		message=(u"El estudio no tiene asignada una dirección de e-mail. Por favor verifique.").encode('utf-8')		
		self.assertEqual(response.content,message)		
		self.assertEqual(len(mail.outbox),0)
	
		
class SuscriptoresTest(TestCase):
	def setUp(self):
		self.config = mommy.make(Configuracion,id=000)
		self.config.save()
		self.user = User.objects.create_user(username='juanma', password='qwerty')
		self.factory = RequestFactory()
		self.usprfl = UserProfile(user=self.user,id_responsable=1,tipoUsr=0)            	
		self.usprfl.save()
		self.client = Client()
		self.client.force_login(self.user)
		self.request = self.factory.get('/')
		self.request.user = self.user
		self.cuotas = mommy.make(Cuotas,id_padron=1,padron='001',id_responsable=1,_quantity=3)
		self.cuotas2 = mommy.make(Cuotas,id_padron=2,padron='001',id_responsable=2,_quantity=3)
			
	def test_get_suscriptor(self):
		self.suscriptores = mommy.make(Suscriptores,id_padron=1)
		s = get_suscriptor(1)
		self.assertNotEqual(s,None)
		s = get_suscriptor()
		self.assertEqual(s,None)

	def test_suscripcion_alta_nueva(self):
		response = self.client.get(reverse('suscripcion_alta',kwargs={'idp':1}))		
		msjs = [m.level for m in messages.get_messages(response.wsgi_request)]
		self.assertIn(messages.SUCCESS, msjs)		
		s = Suscriptores.objects.filter(id_padron=1).first()
		self.assertNotEqual(s,None)
		self.assertEqual(s.fecha_alta,hoy)
		self.assertEqual(s.fecha_baja,None)
	
	def test_suscripcion_alta_edicion(self):
		self.suscriptor = mommy.make(Suscriptores,id_padron=1,fecha_alta=date(2020,1,1),fecha_baja=None)
		response = self.client.get(reverse('suscripcion_alta',kwargs={'idp':1}))
		msjs = [m.level for m in messages.get_messages(response.wsgi_request)]
		self.assertIn(messages.SUCCESS, msjs)
		s = Suscriptores.objects.filter(id_padron=1).first()
		self.assertNotEqual(s,None)
		self.assertEqual(s.fecha_alta,hoy)
		self.assertEqual(s.fecha_baja,None)	
	
	def test_suscripcion_alta_error(self):
		response = self.client.get(reverse('suscripcion_alta',kwargs={'idp':3}))		
		msjs = [m.level for m in messages.get_messages(response.wsgi_request)]
		self.assertIn(messages.ERROR, msjs)
		
	def test_suscripcion_nopuedeVer(self):
		# self.suscriptor = mommy.make(Suscriptores,id_padron=2,fecha_alta=date(2020,1,1),fecha_baja=None)		
		response = self.client.get(reverse('suscripcion_alta',kwargs={'idp':2}))		
		self.assertEqual(response.status_code,302)

	def test_suscripcion_baja(self):
		self.suscriptor = mommy.make(Suscriptores,id_padron=1,fecha_alta=date(2020,1,1),fecha_baja=None)
		response = self.client.get(reverse('suscripcion_baja',kwargs={'idp':1}))		
		msjs = [m.level for m in messages.get_messages(response.wsgi_request)]
		self.assertIn(messages.SUCCESS, msjs)		
		s = Suscriptores.objects.filter(id_padron=1).first()
		self.assertNotEqual(s,None)
		self.assertEqual(s.fecha_baja,hoy)

	def test_suscripcion_bajaError(self):
		self.suscriptor = mommy.make(Suscriptores,id_padron=1,fecha_alta=date(2020,1,1),fecha_baja=None)
		response = self.client.get(reverse('suscripcion_baja',kwargs={'idp':2}))		
		msjs = [m.level for m in messages.get_messages(response.wsgi_request)]
		self.assertIn(messages.ERROR, msjs)		
		s = Suscriptores.objects.filter(id_padron=3).first()
		self.assertEqual(s,None)

		response = self.client.get(reverse('suscripcion_baja',kwargs={'idp':3}))		
		msjs = [m.level for m in messages.get_messages(response.wsgi_request)]
		self.assertIn(messages.ERROR, msjs)
		
# from urllib import urlencode	
url = "%s?cuotas[]=%s&cuotas[]=%s" % (reverse("pago"), 1, 2)
url_exito = "%s?cuotas[]=%s&cuotas[]=%s" % (reverse("pago_exito"), 1, 2)
class PagoOnLineTest(TestCase):
	def setUp(self):
		self.config = mommy.make(Configuracion,id=000)
		self.config.save()
		self.user = User.objects.create_user(username='juanma', password='qwerty')
		self.factory = RequestFactory()
		self.usprfl = UserProfile(user=self.user,id_responsable=1,tipoUsr=0)            	
		self.usprfl.save()
		self.client = Client()
		self.client.force_login(self.user)
		self.request = self.factory.get('/')
		self.request.user = self.user
		dri = mommy.make(Tributo,id_tributo=6,descripcion='DReI',abreviatura='DRI')
		tgiu = mommy.make(Tributo,id_tributo=1,descripcion='TGIU',abreviatura='TGIU')
		self.cuota = mommy.make(Cuotas,id_cuota=1,id_padron=1,padron='001',id_responsable=1,tributo=dri,cuota='1')
		self.cuota2 = mommy.make(Cuotas,id_cuota=2,id_padron=1,padron='001',id_responsable=1,tributo=tgiu,cuota='1')
		self.cuota3 = mommy.make(Cuotas,id_cuota=3,id_padron=2,padron='002',id_responsable=1,tributo=tgiu,cuota='2')		
		self.boleta = mommy.make(DriBoleta,id_cuota=self.cuota,id_padron=1,anio=self.cuota.anio,mes=self.cuota.cuota)
			
	def test_solo_ajax(self):
		"""
		Sin Respuesta AJAX
		"""        
		response = self.client.get(reverse('pago'))		
		self.assertEqual(response.status_code,200)
		message=(u"ERROR sólo AJAX").encode('utf-8')		
		self.assertEqual(response.content,message)		
	
	def test_pagos_cuotas(self):		
		"""
		Respuesta AJAX
		""" 
		response = self.client.get(url,HTTP_X_REQUESTED_WITH='XMLHttpRequest')		
		self.assertEqual(response.status_code,200)		
		message=(u"ERROR sólo AJAX").encode('utf-8')
		self.assertNotEqual(response.content,message)
		self.assertNotEqual(response.content,'[]')

	def test_pagos_cuotas_error(self):		
		"""
		Error en los parametros
		""" 
		url = "%s?cuota[]=%s&cu" % (reverse("pago"), 1)		
		response = self.client.get(url,HTTP_X_REQUESTED_WITH='XMLHttpRequest')		
		self.assertEqual(response.status_code,200)						
		self.assertEqual(response.content,'[]')		

	def test_pagos_exito(self):		
		"""
		Exito en la respuesta de Cajero24
		""" 
		response = self.client.get(url_exito)		
		cuotas = len(Cuotas.objects.filter(id_cuota__in=[1,2],estado=1000))				
		self.assertNotEqual(cuotas,0)
		self.assertRedirects(response, reverse('ver_cuotas', kwargs={'idp':1}))

	def test_pagos_exito_error(self):		
		"""
		Error procesando la respuesta de éxito de Cajero24
		""" 
		url_exito = "%s?cuota[]=%s&cu" % (reverse("pago_exito"), 1)		
		response = self.client.get(url_exito)		
		cuotas = len(Cuotas.objects.filter(id_cuota__in=[1,2],estado=1000))				
		self.assertEqual(cuotas,0)
		self.assertRedirects(response, reverse('padrones_responsable'))

	def test_pagos_error(self):		
		"""
		Error procesando la respuesta de éxito de Cajero24
		""" 
		response = self.client.get(reverse('pago_error',kwargs={'idp':0}))	
		self.assertRedirects(response, reverse('ver_cuotas', kwargs={'idp':0}))
		
import decimal
from decimal import Decimal		
class PunitoriosTest(TestCase):
	"""
	punitorios(c,fecha_punitorios,importe)
	"""
	def setUp(self):		
		self.config = mommy.make(Configuracion,id=000,longitudCodigoBarra=48,tipo_punitorios=2,punitorios=0.02)
		self.urbano = mommy.make(Tributo,id_tributo=1,tipo_interes=None,interes=None,descripcion='TGIs',abreviatura='TGIU',correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      
		self.rural = mommy.make(Tributo,id_tributo=2,tipo_interes=None,interes=None,descripcion='TGIs',abreviatura='TGIR',correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      		
		self.drei = mommy.make(Tributo,id_tributo=6,tipo_interes=None,interes=None,descripcion='DReI',abreviatura='DRI',correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      		
		self.cuota_urbano = mommy.make(Cuotas,id_cuota=1,tributo=self.urbano,cuota='1',anio=2020,saldo=100,vencimiento=date(2020,1,15),segundo_vencimiento=date(2020,2,15),id_padron=1,padron='001',id_responsable=1) 						
		self.cuota_rural = mommy.make(Cuotas,id_cuota=2,tributo=self.rural,cuota='1',anio=2020,saldo=100,vencimiento=date(2020,1,15),segundo_vencimiento=date(2020,2,15),id_padron=2,padron='001',id_responsable=1) 
		self.cuota_drei = mommy.make(Cuotas,id_cuota=3,tributo=self.drei,cuota='1',anio=2020,saldo=100,vencimiento=date(2020,1,15),segundo_vencimiento=date(2020,1,15),id_padron=3,padron='001',id_responsable=1) 

	def test_configuracion(self):		
		Configuracion.objects.all().delete()
		p = punitorios(self.cuota_urbano,hoy,None)
		self.assertEqual(p,0)

	def test_interes_config_2(self):		
		""" Sin vencer """		
		p = punitorios(self.cuota_urbano,date(2020,1,1),None)
		self.assertEqual(p,0)

		""" Vencido 1er venc """		
		p1 = punitorios(self.cuota_urbano,date(2020,1,25),None)
		p2 = punitorios(self.cuota_urbano,self.cuota_urbano.segundo_vencimiento,None)
		self.assertEqual(p1,p2)

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_urbano,date(3000,1,1),None)		
		tot = Decimal(23837.76).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

		""" DREI """
		""" Sin vencer """		
		p = punitorios(self.cuota_drei,date(2020,1,1),None)
		self.assertEqual(p,0)		

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_drei,date(3000,1,1),None)		
		tot = Decimal(23837.70).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

	def test_interes_config_1(self):		
		self.config = mommy.make(Configuracion,id=000,longitudCodigoBarra=48,tipo_punitorios=1,punitorios=0.02)
		""" Sin vencer """		
		p = punitorios(self.cuota_urbano,date(2020,1,1),None)
		self.assertEqual(p,0)

		""" Vencido 1er venc """		
		p1 = punitorios(self.cuota_urbano,date(2020,2,25),None)		
		p2 = punitorios(self.cuota_urbano,self.cuota_urbano.segundo_vencimiento,None)
		self.assertEqual(p1,p2)

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_urbano,date(3000,1,1),None)				
		tot = Decimal(23860.00).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

		""" DREI """
		""" Sin vencer """		
		p = punitorios(self.cuota_drei,date(2020,1,1),None)
		self.assertEqual(p,0)		

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_drei,date(3000,1,1),None)		
		tot = Decimal(23860.00).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

	def test_interes_config_4(self):		
		self.config = mommy.make(Configuracion,id=000,longitudCodigoBarra=48,tipo_punitorios=4,punitorios=0.02)
		""" Sin vencer """		
		p = punitorios(self.cuota_urbano,date(2020,1,1),None)
		self.assertEqual(p,0)

		""" Vencido 1er venc """		
		p1 = punitorios(self.cuota_urbano,date(2020,2,25),None)		
		p2 = punitorios(self.cuota_urbano,self.cuota_urbano.segundo_vencimiento,None)
		self.assertEqual(p1,p2)

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_urbano,date(3000,1,1),None)				
		tot = Decimal(23862.00).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

		""" DREI """
		""" Sin vencer """		
		p = punitorios(self.cuota_drei,date(2020,1,1),None)
		self.assertEqual(p,0)		

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_drei,date(3000,1,1),None)		
		tot = Decimal(23862.00).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)


	def test_interes_config_10(self):		
		self.config = mommy.make(Configuracion,id=000,longitudCodigoBarra=48,tipo_punitorios=2,punitorios=0.03)		
		self.urbano = mommy.make(Tributo,id_tributo=1,tipo_interes=10,interes=0.03,descripcion='TGIs',abreviatura='TGIU',correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      
		self.trib_interes_1 = mommy.make(TributoInteres,id_tributo=1,desde=date(1900,1,1),hasta=date(2020,1,31),tipo_interes=3,interes=0.02) 						
		self.trib_interes_2 = mommy.make(TributoInteres,id_tributo=1,desde=date(2020,2,1),hasta=date(3000,1,1),tipo_interes=3,interes=0.03)
		self.cuota_urbano.tributo= self.urbano
		self.cuota_urbano.saldo= Decimal(2269.62)
		self.cuota_urbano.vencimiento = date(2020,2,17)
		self.cuota_urbano.segundo_vencimiento = date(2020,3,17)
		self.cuota_urbano.save()

		""" Sin vencer """		
		p = punitorios(self.cuota_urbano,date(2020,1,1),None)
		self.assertEqual(p,0)

		""" Vencido 1er venc """		
		p1 = punitorios(self.cuota_urbano,date(2020,2,25),None)				
		p2 = punitorios(self.cuota_urbano,self.cuota_urbano.segundo_vencimiento,None)
		self.assertEqual(p1,p2)

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_urbano,date(3000,1,1),None)				
		tot = Decimal(812276.57).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

		""" DREI """
		""" Sin vencer """		
		p = punitorios(self.cuota_drei,date(2020,1,1),None)
		self.assertEqual(p,0)		

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_drei,date(3000,1,1),None)		
		tot = Decimal(35792.40).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

	def test_interes_config_11(self):		
		self.config = mommy.make(Configuracion,id=000,longitudCodigoBarra=48,tipo_punitorios=2,punitorios=0.03)		
		self.urbano = mommy.make(Tributo,id_tributo=1,tipo_interes=11,interes=0.03,descripcion='TGIs',abreviatura='TGIU',interes_2ven=0.00,correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      
		self.trib_interes_1 = mommy.make(TributoInteres,id_tributo=1,desde=date(1900,1,1),hasta=date(2020,1,31),tipo_interes=3,interes=0.02) 						
		self.trib_interes_2 = mommy.make(TributoInteres,id_tributo=1,desde=date(2020,2,1),hasta=date(3000,1,1),tipo_interes=3,interes=0.03)
		self.cuota_urbano.tributo= self.urbano
		self.cuota_urbano.saldo= Decimal(2269.62)
		self.cuota_urbano.vencimiento = date(2020,2,17)
		self.cuota_urbano.segundo_vencimiento = date(2020,3,17)
		self.cuota_urbano.save()

		""" Sin vencer """		
		p = punitorios(self.cuota_urbano,date(2020,1,1),None)
		self.assertEqual(p,0)

		""" Vencido 1er venc """		
		p1 = punitorios(self.cuota_urbano,date(2020,2,25),None)				
		p2 = punitorios(self.cuota_urbano,self.cuota_urbano.segundo_vencimiento,None)
		self.assertTrue(p1>0)
		self.assertTrue(p2>p1)

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_urbano,date(3000,1,1),None)				
		tot = Decimal(812276.57).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

		""" DREI """
		""" Sin vencer """		
		p = punitorios(self.cuota_drei,date(2020,1,1),None)
		self.assertEqual(p,0)		

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_drei,date(3000,1,1),None)		
		tot = Decimal(35792.40).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

	def test_interes_config_99(self):		
		self.config = mommy.make(Configuracion,id=000,longitudCodigoBarra=48,tipo_punitorios=2,punitorios=0.02)		
		self.urbano = mommy.make(Tributo,id_tributo=1,tipo_interes=99,interes=0.05,descripcion='TGIs',abreviatura='TGIU',interes_2=0.10,vence_dias2=60,correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      
		self.dri = mommy.make(Tributo,id_tributo=6,tipo_interes=99,interes=0.05,descripcion='TGIs',abreviatura='TGIU',interes_2=0.10,vence_dias2=60,correr_venc_fdesde=date(2020,1,1),correr_venc_fhasta=date(2020,2,15),correr_venc_dias=0)      
		self.cuota_urbano.tributo= self.urbano
		self.cuota_urbano.saldo= Decimal(220.90)
		self.cuota_urbano.vencimiento = date(2020,2,11)
		self.cuota_urbano.segundo_vencimiento = date(2020,3,11)
		self.cuota_urbano.save()
		self.cuota_drei.tributo= self.dri
		self.cuota_drei.saldo= Decimal(220.90)
		self.cuota_drei.vencimiento = date(2020,2,11)
		self.cuota_drei.segundo_vencimiento = date(2020,3,11)
		self.cuota_drei.save()

		""" Sin vencer """		
		p = punitorios(self.cuota_urbano,date(2020,1,1),None)
		self.assertEqual(p,0)

		""" Vencido 1er venc """		
		p1 = punitorios(self.cuota_urbano,date(2020,2,25),None)				
		p2 = punitorios(self.cuota_urbano,self.cuota_urbano.segundo_vencimiento,None)		
		self.assertTrue(p1==p2)		

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_urbano,date(3000,1,1),None)				
		tot = Decimal(52666.76).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)

		""" DREI """
		""" Sin vencer """		
		p = punitorios(self.cuota_drei,date(2020,1,1),None)
		self.assertEqual(p,0)		

		""" Vencido 1er venc """		
		p1 = punitorios(self.cuota_drei,date(2020,3,25),None)				
		p2 = punitorios(self.cuota_drei,self.cuota_drei.segundo_vencimiento,None)		
		self.assertTrue(p1==p2)		

		""" Vencido 2do venc """		
		p = punitorios(self.cuota_drei,date(3000,1,1),None)		
		tot = Decimal(52666.76).quantize(Decimal("0.01"),decimal.ROUND_HALF_UP)
		self.assertEqual(p,tot)



		

	
	
		
		


		





