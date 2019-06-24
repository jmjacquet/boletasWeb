# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from .utilidades import ESTADOS,TIPOUSR
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import *

class Tributo(models.Model):
    id_tributo = models.IntegerField(primary_key=True,null=False)
    descripcion = models.CharField(max_length=80, blank=True)
    abreviatura = models.CharField(max_length=10, blank=True)
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
    desde = models.DateField()
    hasta = models.DateField()
    tipo_interes = models.IntegerField(blank=True, null=True)
    interes = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    class Meta:
        db_table = 'tributo_interes'        
        unique_together = ('id_tributo', 'desde','hasta')

class Responsables(models.Model):
    id_responsable = models.IntegerField(primary_key=True,db_index=True)
    nombre = models.CharField(max_length=100)
    nombre_boleta = models.CharField(max_length=30)
    tipo_doc = models.IntegerField(blank=True, null=True)
    nrodocu = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True)
    calle = models.CharField(max_length=35, blank=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.CharField(max_length=2, blank=True)
    depto = models.CharField(max_length=2, blank=True)
    localidad = models.CharField(max_length=25, blank=True)
    provincia = models.IntegerField(blank=True, null=True)
    codseg = models.CharField(max_length=10)
    class Meta:
        db_table = 'responsables'

    def __unicode__(self):
        return u'%s - %s (%s)' % (self.nombre,self.nrodocu,self.codseg)

class Sinc(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField(db_index=True)
    hora = models.TimeField()
    ultimo_id = models.IntegerField()
    class Meta:
        db_table = 'sinc'

class SincPers(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    ultimo_id = models.IntegerField()
    class Meta:
        db_table = 'sinc_pers'

class Cuotas(models.Model):
    id_cuota = models.IntegerField(primary_key=True,db_index=True)
    id_responsable = models.ForeignKey('Responsables', db_column='id_responsable')
    tributo = models.ForeignKey('Tributo', db_column='tributo')
    id_unidad = models.IntegerField()
    anio = models.IntegerField()
    cuota = models.CharField(max_length=4)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)
    vencimiento = models.DateField()
    id_padron = models.CharField(max_length=20,db_index=True)
    padron = models.CharField(max_length=20,db_index=True)
    fechapago = models.DateField(blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS)
    segundo_vencimiento = models.DateField(null=True)
    #convenio = models.IntegerField(null=True)
    class Meta:
        db_table = 'cuotas'

    def __unicode__(self):
        return u'%s --> %s' % (self.padron, self.id_padron)
    @property
    def get_estado(self):
        now = datetime.date.today()
        delta = self.vencimiento - now
        if self.saldo<=0:
            e = 'PAGADO'
        elif ((delta.days < 0)and(self.estado==0)):
            e = 'VENCIDO'
        else:
            e=self.get_estado_display
        return e

    def get_boleta_venc(self):
        try:
            boleta = DriBoleta.objects.get(id_cuota=self.id_cuota)
        except:
            boleta = None
        if boleta:
            now = datetime.date.today()
            return self.fechapago < now                   
        else:
            return False

    def get_boletas(self):
        try:
            boletas = DriBoleta.objects.filter(id_cuota=self.id_cuota)
        except:
            boletas = None
        return boletas
   
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
    id_estudioc = models.ForeignKey('DriEstudio', db_column='id_estudioc')
    id_padron = models.IntegerField(blank=True, null=True,db_index=True)
    class Meta:
        db_table = 'dri_estudio_padron'

class DriActividades(models.Model):
    id_actividad = models.IntegerField(primary_key=True)
    denominacion = models.CharField(max_length=200, blank=True)
    codigo = models.CharField(max_length=10, blank=True)
    id_rubro = models.CharField(max_length=10, blank=True)
    alicuota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    concepto = models.IntegerField(blank=True, null=True)
    id_subrubro = models.CharField(max_length=10, blank=True)
    minimo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)    

    class Meta:
        db_table = 'dri_actividades'
    def __unicode__(self):
        return u'%s - %s' % (self.codigo, self.denominacion)

class DriPadronActividades(models.Model):
    id = models.AutoField(primary_key=True)
    id_padron = models.IntegerField(null=False)
    id_actividad = models.ForeignKey('DriActividades', db_column='id_actividad',null=False)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    principal = models.CharField(max_length=1, blank=True)
    monto_minimo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    expediente = models.CharField(max_length=20, blank=True)
    id_sinc = models.IntegerField()
    class Meta:
        db_table = 'dri_padron_actividades'
        ordering = ['-principal','id_padron']
        unique_together = ('id_padron', 'id_actividad','fecha_inicio')

    def __unicode__(self):
        if self.principal=='S':
           return u'(*) %s - %s' % (self.id_actividad.codigo,self.id_actividad.denominacion)
        else:
            return u'%s - %s' % (self.id_actividad.codigo,self.id_actividad.denominacion)

    def verDetalleActiv(self):
        ida=self.id_actividad
        idp=self.id_padron
        try:
            actPadr = DriPadronActividades.objects.filter(id_padron=idp,id_actividad=ida).select_related('id_actividad').first()
            if actPadr.principal=='S':
               detalle = u'(*) %s - %s' % (actPadr.id_actividad.codigo,actPadr.id_actividad.denominacion)
            else:
                detalle = u'%s - %s' % (actPadr.id_actividad.codigo,actPadr.id_actividad.denominacion)
        except:
            detalle = '(ACTIVIDAD NO ESPECIFICADA)'

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

    @property
    def get_vencido(self):
        now = datetime.date.today()
        delta = self.fechapago - now       
        return delta.days < 0

class DriBoleta_actividades(models.Model):
    id = models.AutoField(primary_key=True)
    id_boleta = models.ForeignKey('DriBoleta', db_column='id_boleta')
    id_actividad = models.ForeignKey('DriActividades', db_column='id_actividad')
    base = models.DecimalField(max_digits=15, decimal_places=2)
    alicuota = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    minimo = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    impuesto = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    activ_descr = models.CharField(max_length=200,blank=True, null=True)
    class Meta:
        db_table = 'dri_boleta_actividades'

    def __unicode__(self):
        return u'%s %s' % (self.id_boleta.id_padron,self.id_actividad)

    def verDetalleActiv(self):
        ida=self.id_actividad
        idp=self.id_boleta.id_padron
        try:
            actPadr = DriPadronActividades.objects.filter(id_padron=idp,id_actividad=ida).select_related('id_actividad').first()
            if actPadr.principal=='S':
               detalle = u'(*) %s - %s' % (actPadr.id_actividad.codigo,actPadr.id_actividad.denominacion)
            else:
                detalle = u'%s - %s' % (actPadr.id_actividad.codigo,actPadr.id_actividad.denominacion)
        except:
            detalle = '(ACTIVIDAD NO ESPECIFICADA)'
        return detalle[:200]


### Drei DDJJ Anual

class DriDDJJA(models.Model):
    id_ddjj = models.AutoField(primary_key=True)
    id_padron = models.IntegerField() 
    anio = models.IntegerField()    
    total_imponible = models.DecimalField(max_digits=15, decimal_places=2)
    total_impuestos = models.DecimalField(max_digits=15, decimal_places=2)
    total_adicionales = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_carga = models.DateField('Fecha Çarga', auto_now_add = True,blank=True, null=True)
    fecha_confirmado = models.DateField(blank=True, null=True)
    fecha_impresa = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'dri_ddjj'
    def __unicode__(self):
        return u'%s %s %s' % (self.id_ddjj,self.id_padron,self.anio)

class DriDDJJA_actividades(models.Model):
    id = models.AutoField(primary_key=True)
    periodo = models.IntegerField()    
    id_boleta = models.IntegerField() 
    id_ddjj = models.ForeignKey('DriDDJJA', db_column='id_ddjj')
    id_actividad = models.ForeignKey('DriActividades', db_column='id_actividad')
    base = models.DecimalField(max_digits=15, decimal_places=2)
    alicuota = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    minimo = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    impuesto = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    adicionales = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    activ_descr = models.CharField(max_length=200,blank=True, null=True)
    class Meta:
        db_table = 'dri_ddjj_actividades'

    def __unicode__(self):
        return u'%s %s' % (self.id_boleta.id_padron,self.id_actividad)

#******************************************************************************************

class WEB_Liquidacion(models.Model):
    id_liquidacion = models.AutoField(primary_key=True)
    id_unidad = models.IntegerField()
    tipo = models.IntegerField('Tipo Liquidacion', default=1)
    vencimiento = models.DateField()
    nominal = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)   
    total = models.DecimalField(max_digits=10, decimal_places=2)   
    pasado_a_cnv = models.IntegerField(default=0)  
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    usuario = models.CharField(max_length=30)
    fecha_punitorios = models.DateField(blank=True, null=True)
    punitorios = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'web_liquidacion'


class WEB_Liquidacion_ctas(models.Model):
    id_liquidacion = models.ForeignKey('WEB_Liquidacion', db_column='id_liquidacion')
    id_cuota =  models.ForeignKey('Cuotas', db_column='id_cuota',null=True)
    tributo = models.IntegerField()
    nominal = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)   

    class Meta:
        db_table = 'web_liquidacion_ctas'

#******************************************************************************************

#Tabla de la Base de Configuracion
class Configuracion(models.Model):
    id = models.IntegerField(primary_key=True,db_index=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    varios1 = models.CharField(max_length=100, blank=True)
    db = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    directorio = models.CharField(max_length=100)
    punitorios = models.DecimalField(max_digits=15, decimal_places=4)
    tipo_punitorios = models.IntegerField()
    linea1 = models.CharField(max_length=100, blank=True)
    linea2 = models.CharField(max_length=100, blank=True)
    link_retorno = models.CharField(max_length=100, blank=True)
    mantenimiento = models.IntegerField()
    ncuerpo1 = models.CharField(max_length=20, blank=True)
    ncuerpo2 = models.CharField(max_length=20, blank=True)
    ncuerpo3 = models.CharField(max_length=20, blank=True)
    codigo_visible = models.CharField(max_length=1, blank=True)
    debug = models.CharField(max_length=1, blank=True)
    diasextravencim = models.IntegerField(db_column='diasExtraVencim', blank=True, null=True) # Field name made lowercase.
    alicuota_unidad = models.CharField(max_length=10, blank=True)
    alicuota_coeficiente = models.DecimalField(max_digits=15, decimal_places=2)
    detalleContrib = models.CharField(max_length=300, blank=True)
    ver_unico_padron = models.CharField(max_length=1, blank=True,default='N')
    liquidacion_web = models.CharField(max_length=1, blank=True,default='N')
    codigo_link_visible = models.CharField(max_length=1, blank=True,default='S')
    longitudCodigoBarra = models.IntegerField(db_column='longitudCodigoBarra',default=48, blank=True, null=True) # Field name made lowercase.
    minimo_por_activ = models.CharField(max_length=1, blank=True,default='S')
    alicuota_fija = models.CharField(max_length=1, blank=True,default='N')
    puede_rectificar = models.CharField(max_length=1, blank=True,default='N')
    class Meta:
        db_table = 'configuracion'
    
    def __unicode__(self):
        return u'%s' % (self.nombre)

#Tabla de Usuario con datos Extra
class UserProfile(models.Model):
    id_responsable = models.IntegerField(blank=True, null=True)
    id_estudioc = models.IntegerField(blank=True, null=True)
    tipoUsr = models.IntegerField(choices=TIPOUSR,default=0)
    user = models.OneToOneField(User)

    class Meta:
        db_table = 'user_profile'

    def __unicode__(self):
        return self.user.username


# from django.db.models.signals import post_save
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile, created = UserProfile.objects.get_or_create(user=instance,tipoUsr=2)        

# post_save.connect(create_user_profile, sender=User)
