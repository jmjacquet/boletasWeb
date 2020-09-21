# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase,RequestFactory
from model_mommy import mommy
from django.test.client import Client
from tadese.models import Configuracion,UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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



    def test_municipio(self):
        response = self.client.get(reverse('municipio'))
    	self.assertEqual(response.status_code, 200)

    def test_padrones_responsable(self):
        response = self.client.get(reverse('padrones_responsable'))
    	self.assertEqual(response.status_code, 200)

    # def test_ver_cuotas(self):
    #     response = self.client.get(reverse('ver_cuotas'))
    # 	self.assertNotEqual(response.status_code, 200)
        