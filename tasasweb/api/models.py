# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Cuotas(models.Model):
    id_cuota = models.PositiveIntegerField(primary_key=True,db_index=True,)
    id_responsable = models.IntegerField()
    #tributo = models.ForeignKey('Tributo', db_column='tributo',related_name='cuota_tributo')
    tributo = models.IntegerField()
    id_unidad = models.IntegerField()
    anio = models.IntegerField()
    cuota = models.CharField(max_length=4)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)
    vencimiento = models.DateField()
    id_padron = models.CharField(max_length=20,db_index=True, null=True)
    padron = models.CharField(max_length=20,db_index=True, null=True)
    fechapago = models.DateField(blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS, null=True)
    segundo_vencimiento = models.DateField(null=True)

    nombre = models.CharField(max_length=100,blank=True, null=True)
    nombre_boleta = models.CharField(max_length=30,blank=True, null=True)
    nrodocu = models.CharField(max_length=30, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    calle = models.CharField(max_length=35, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.CharField(max_length=2, blank=True, null=True)
    depto = models.CharField(max_length=2, blank=True, null=True)
    localidad = models.CharField(max_length=25, blank=True, null=True)   
    codseg = models.CharField(max_length=10, null=True)

    fecha_audit = models.DateTimeField(auto_now = True, null=True) 
        
    class Meta:
        db_table = 'cuotas'
        ordering = ['-anio','-cuota','-id_cuota']