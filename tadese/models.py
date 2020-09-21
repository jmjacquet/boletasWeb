# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from .utilidades import ESTADOS,TIPOUSR,correr_vencimiento
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import *

class Tributo(models.Model):
    id_tributo = models.IntegerField(primary_key=True,null=False)
    descripcion = models.CharField(max_length=80, blank=True,null=True)
    abreviatura = models.CharField(max_length=10, blank=True,null=True)
    cajaimporte = models.CharField(db_column='CAJAIMPORTE', max_length=1, blank=True) # Field name made lowercase.
    reporte = models.CharField(db_column='REPORTE', max_length=30, blank=True) # Field name made lowercase.
    tipo_interes = models.IntegerField(db_column='TIPO_INTERES', blank=True, null=True) # Field name made lowercase.
    interes = models.DecimalField(db_column='INTERES', max_digits=15, decimal_places=6, blank=True, null=True) # Field name made lowercase.
    formato = models.CharField(db_column='FORMATO', max_length=20, blank=True) # Field name made lowercase.
    bonificacion = models.DecimalField(db_column='BONIFICACION', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    vence_dias = models.IntegerField(db_column='VENCE_DIAS', blank=True, null=True) # Field name made lowercase.
    vence_meses = models.IntegerField(db_column='VENCE_MESES', blank=True, null=True) # Field name made lowercase.
    interes_2ven = models.DecimalField(db_column='INTERES_2VEN', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    nobonificable = models.DecimalField(db_column='NOBONIFICABLE', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    interes_2 = models.DecimalField(db_column='INTERES_2', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    vence_dias2 = models.IntegerField(db_column='VENCE_DIAS2', blank=True, null=True)  # Field name made lowercase.
    suscripcion = models.CharField(db_column='SUSCRIPCION', max_length=1,null=True, blank=True)

    correr_venc_fdesde = models.DateField(db_column='CORRER_VENC_FDESDE',blank=True, null=True)
    correr_venc_fhasta = models.DateField(db_column='CORRER_VENC_FHASTA',blank=True, null=True)
    correr_venc_dias = models.IntegerField(db_column='CORRER_VENC_DIAS', blank=True, null=True)

    class Meta:
        db_table = 'tributo'

    def __unicode__(self):
        return u'%s' % (self.descripcion)

    @property
    def get_abreviatura(self):
        return self.abreviatura

class TributoInteres(models.Model):
    # id = models.AutoField(primary_key=True)
    id_tributo = models.IntegerField()
    desde = models.DateField( null=True)
    hasta = models.DateField( null=True)
    tipo_interes = models.IntegerField(blank=True, null=True)
    interes = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    class Meta:
        db_table = 'tributo_interes'        
        unique_together = ('id_tributo', 'desde','hasta')

    def __unicode__(self):
        return u'%s - %s' % (self.id_tributo,self.interes)

class Cuotas(models.Model):
    id_cuota = models.PositiveIntegerField(primary_key=True,db_index=True,)
    id_responsable = models.IntegerField()
    tributo = models.ForeignKey('Tributo', db_column='tributo')
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

    def __unicode__(self):
        return u'%s --> %s' % (self.padron, self.id_padron)

    def get_datos(self):
        return u'%s/%s-%s(%s)' % (self.cuota,self.anio,self.padron, self.tributo.abreviatura)

    @property
    def tributo_nombre(self):
        return self.tributo

    @property
    def tributo_abreviatura(self):
        return self.tributo.get_abreviatura
        
    @property
    def get_estado(self):
        now = datetime.date.today()
        dias = (self.vencimiento - now).days
        if self.saldo<=0:
            e = 'PAGADO'
        elif ((dias < 0)and(self.estado==0)):
            e = 'VENCIDO'
        else:
            e=self.get_estado_display()
        return e

    @property
    def get_vencimiento(self):# pragma: no cover
        vencimiento = correr_vencimiento(self.vencimiento,self.segundo_vencimiento,self.tributo)[0]
        return vencimiento

    @property
    def get_vencimiento2(self): # pragma: no cover        
        vencimiento = correr_vencimiento(self.vencimiento,self.segundo_vencimiento,self.tributo)[1]
        return vencimiento

    @property
    def get_boleta_venc(self):
        try:
            boleta = DriBoleta.objects.get(id_cuota=self.id_cuota)
        except:
            boleta = None
        if boleta:
            now = datetime.date.today()            
            return now <= boleta.fechapago
        else:
            return False

    def get_responsable(self):
        return u'%s (%s)' % (self.nombre,self.nrodocu)



class DriEstudio(models.Model):
    id_estudioc = models.IntegerField(primary_key=True)
    denominacion = models.CharField(db_column='Denominacion', max_length=100, null=True) # Field name made lowercase.
    usuario = models.CharField(max_length=30, blank=True, null=True)
    clave = models.CharField(max_length=30, blank=True, null=True)
    numero = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=100, blank=True,null=True)
    class Meta:
        db_table = 'dri_estudio'
    def __unicode__(self):
        return u'%s - %s' % (self.numero, self.denominacion)

class DriEstudioPadron(models.Model):
    id_negocio = models.IntegerField(primary_key=True)
    id_estudioc = models.ForeignKey('DriEstudio', db_column='id_estudioc',on_delete=models.CASCADE)
    id_padron = models.IntegerField(blank=True, null=True,db_index=True)
    class Meta:
        db_table = 'dri_estudio_padron'

class DriCuotaActividad(models.Model):
    id_cuota_actividad = models.AutoField(primary_key=True)
    id_padron = models.IntegerField(null=True)
    id_actividad = models.IntegerField(null=True)
    denominacion = models.CharField(max_length=200, blank=True)
    codigo = models.CharField(max_length=10, blank=True)   
    alicuota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)    
    minimo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)    
    actividad_principal = models.CharField(max_length=1, blank=True, null=True)
    id_cuota = models.ForeignKey('Cuotas', db_column='id_cuota',related_name='actividad_cuota',on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'dri_cuota_actividad'
        ordering = ['-actividad_principal','denominacion','id_padron']
    
    def __unicode__(self):
        detalle = u'%s - %s' % (self.codigo,self.denominacion)
        if self.actividad_principal=='S':
        	detalle = u'(*) %s - %s' % (self.codigo,self.denominacion)                   
        return detalle[:200]

    def get_actividad(self):
        detalle = u'%s - %s' % (self.codigo,self.denominacion)
        if self.actividad_principal=='S':
            detalle = u'(*) %s - %s' % (self.codigo,self.denominacion)                   
        return detalle[:200]

### Boletas DREI Liquidación
class DriBoleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    id_padron = models.IntegerField(db_index=True) 
    anio = models.IntegerField()
    mes = models.IntegerField()
    vencimiento = models.DateField(auto_now = True)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    fechapago = models.DateField('Fecha Generado', auto_now  = True,blank=True, null=True)
    recargo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    derecho_neto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tasa_salud_publ = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    adic_detalle = models.CharField(max_length=100,blank=True, null=True)
    adic_monto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    retenciones = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    id_cuota = models.ForeignKey('Cuotas', db_column='id_cuota',related_name='boleta_cuota')
    minimo_global = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pago_anterior = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    class Meta:
        db_table = 'dri_boleta'
    def __unicode__(self):
        return u'%s %s %s' % (self.id_padron,self.anio,self.mes)

class DriBoleta_actividades(models.Model):
    id = models.AutoField(primary_key=True)
    id_boleta = models.ForeignKey('DriBoleta', db_column='id_boleta',on_delete=models.CASCADE, null=True)    
    id_actividad = models.IntegerField(null=False)
    base = models.DecimalField(max_digits=15, decimal_places=2)
    alicuota = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    minimo = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    impuesto = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    activ_descr = models.CharField(max_length=200,blank=True, null=True)
    class Meta:
        db_table = 'dri_boleta_actividades'
        default_related_name = 'boleta_actividades'


    def __unicode__(self):
        detalle = u'%s' % (self.activ_descr)        
        return detalle[:200]


#******************************************************************************************

class WEB_Liquidacion(models.Model):# pragma: no cover
    id_liquidacion = models.AutoField(primary_key=True)
    id_unidad = models.IntegerField()
    tipo = models.IntegerField('Tipo Liquidacion', default=1)
    vencimiento = models.DateField()
    nominal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    interes = models.DecimalField(max_digits=10, decimal_places=2, null=True)   
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)   
    pasado_a_cnv = models.IntegerField(default=0)  
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    usuario = models.CharField(max_length=30)
    fecha_punitorios = models.DateField(blank=True, null=True)
    punitorios = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    class Meta:
        db_table = 'web_liquidacion'


class WEB_Liquidacion_ctas(models.Model):# pragma: no cover
    id_liquidacion = models.ForeignKey('WEB_Liquidacion', db_column='id_liquidacion',on_delete=models.CASCADE)
    id_cuota =  models.ForeignKey('Cuotas', db_column='id_cuota',null=True,on_delete=models.CASCADE)
    tributo = models.IntegerField()
    nominal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    interes = models.DecimalField(max_digits=10, decimal_places=2, null=True)   
    class Meta:
        db_table = 'web_liquidacion_ctas'

#******************************************************************************************

#Tabla de la Base de Configuracion
class Configuracion(models.Model):# pragma: no cover
    id = models.PositiveIntegerField(primary_key=True,db_index=True)
    nombre = models.CharField(max_length=100,blank=True, null=True)
    direccion = models.CharField(max_length=100,blank=True, null=True)
    varios1 = models.CharField(max_length=100, blank=True, null=True)    
    punitorios = models.DecimalField(max_digits=15, decimal_places=4,blank=True, null=True)
    tipo_punitorios = models.IntegerField(blank=True, null=True)
    linea1 = models.CharField(max_length=100, blank=True, null=True)
    linea2 = models.CharField(max_length=100, blank=True, null=True)
    link_retorno = models.CharField(max_length=100, blank=True, null=True)
    mantenimiento = models.IntegerField(blank=True, null=True)
    ncuerpo1 = models.CharField(max_length=20, blank=True, null=True)
    ncuerpo2 = models.CharField(max_length=20, blank=True, null=True)
    ncuerpo3 = models.CharField(max_length=20, blank=True, null=True)
    codigo_visible = models.CharField(max_length=1, blank=True)
    debug = models.CharField(max_length=1, blank=True)
    diasextravencim = models.IntegerField(db_column='diasExtraVencim', blank=True, null=True) # Field name made lowercase.
    alicuota_unidad = models.CharField(max_length=10, blank=True, null=True)
    alicuota_coeficiente = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    detalleContrib = models.CharField(max_length=300,  blank=True, null=True)
    ver_unico_padron = models.CharField(max_length=1, blank=True,default='N')
    liquidacion_web = models.CharField(max_length=1, blank=True,default='N')
    codigo_link_visible = models.CharField(max_length=1, blank=True,default='S')
    longitudCodigoBarra = models.IntegerField(db_column='longitudCodigoBarra',default=48, blank=True, null=True) # Field name made lowercase.
    minimo_por_activ = models.CharField(max_length=1, blank=True, null=True,default='S')
    alicuota_fija = models.CharField(max_length=1, blank=True, null=True,default='N')
    puede_rectificar = models.CharField(max_length=1, null=True, blank=True,default='N')
    suscripcion = models.CharField(max_length=1, null=True, blank=True)
    suscripcion_msj = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = 'configuracion'
    
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Configuracion_vars(models.Model):# pragma: no cover
    id = models.AutoField(primary_key=True,db_index=True)
    variable = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    numero = models.DecimalField(max_digits=15, decimal_places=4,blank=True, null=True)
    texto = models.CharField(max_length=1000, null=True, blank=True)
    fecha = models.DateField(blank=True, null=True)    
    class Meta:
        db_table = 'configuracion_vars'
    
    def __unicode__(self):
        return u'%s' % (self.variable)        


#Tabla de Usuario con datos Extra
class UserProfile(models.Model):# pragma: no cover
    id_responsable = models.IntegerField(blank=True, null=True)
    id_estudioc = models.IntegerField(blank=True, null=True)
    tipoUsr = models.IntegerField(choices=TIPOUSR,default=0)
    user = models.OneToOneField(User)

    class Meta:
        db_table = 'user_profile'

    def __unicode__(self):
        return self.user.username

#********************************************************************

#Tabla de Suscriptores
class Suscriptores(models.Model):
    id = models.IntegerField(primary_key=True,db_index=True)
    tributo = models.ForeignKey('Tributo', db_column='tributo')        
    id_padron = models.IntegerField(blank=True, null=True)    
    fecha_alta = models.DateField(auto_now_add = True)
    fecha_baja = models.DateField(null=True)

    class Meta:
        db_table = 'suscriptores'
    
    def __unicode__(self):
        return u'%s' % (self.id)


    @property
    def activa(self):       
        now = datetime.date.today()        
        if not self.fecha_baja:
            return True
        elif (now<self.fecha_baja):
            return True        
        else:
            return False               
