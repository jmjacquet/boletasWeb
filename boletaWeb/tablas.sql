# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class CuotaPeriodos(models.Model):
    id_cuota_periodos = models.IntegerField(primary_key=True)
    anio = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'cuota_periodos'

class Cuotas(models.Model):
    id_cuota = models.IntegerField(primary_key=True)
    id_responsable = models.IntegerField()
    tributo = models.IntegerField()
    id_unidad = models.IntegerField()
    anio = models.IntegerField()
    cuota = models.CharField(max_length=4)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)
    vencimiento = models.DateField()
    id_padron = models.CharField(max_length=20)
    padron = models.CharField(max_length=20)
    fechapago = models.DateField(blank=True, null=True)
    estado = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'cuotas'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'django_site'

class DriActividades(models.Model):
    id_actividad = models.IntegerField()
    denominacion = models.CharField(max_length=200, blank=True)
    codigo = models.CharField(max_length=10, blank=True)
    id_rubro = models.CharField(max_length=10, blank=True)
    alicuota = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    concepto = models.IntegerField(blank=True, null=True)
    id_subrubro = models.CharField(max_length=10, blank=True)
    minimo = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dri_actividades'

class DriActividadesBkp(models.Model):
    id_actividad = models.IntegerField()
    denominacion = models.CharField(max_length=200, blank=True)
    codigo = models.CharField(max_length=10, blank=True)
    id_rubro = models.CharField(max_length=10, blank=True)
    alicuota = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    concepto = models.IntegerField(blank=True, null=True)
    id_subrubro = models.CharField(max_length=10, blank=True)
    minimo = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dri_actividades_bkp'

class DriBoleta(models.Model):
    id_cuota = models.IntegerField(primary_key=True)
    fecha_venc1 = models.DateField()
    importe1 = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_venc2 = models.DateField()
    importe2 = models.DecimalField(max_digits=15, decimal_places=2)
    punitorios = models.DecimalField(max_digits=15, decimal_places=2)
    class Meta:
        managed = False
        db_table = 'dri_boleta'

class DriDclJurada(models.Model):
    id_dcl_jurada = models.IntegerField(primary_key=True)
    id_padron = models.IntegerField()
    padron = models.CharField(max_length=20)
    anio = models.IntegerField(blank=True, null=True)
    periodo = models.IntegerField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=100, blank=True)
    fecha = models.DateField(blank=True, null=True)
    fecha_confirmado = models.DateField(blank=True, null=True)
    importe = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    impresa = models.CharField(max_length=1)
    id_responsable = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'dri_dcl_jurada'

class DriDclJuradaAct(models.Model):
    id_dcl_jurada_act = models.IntegerField(primary_key=True)
    id_dcl_jurada = models.IntegerField()
    periodo = models.IntegerField()
    id_actividad = models.IntegerField()
    importe_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    alicuota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    importe = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dri_dcl_jurada_act'

class DriDclJuradaPeriodo(models.Model):
    anio = models.IntegerField(primary_key=True)
    vencimiento = models.DateField()
    habilitada = models.CharField(max_length=1)
    generar_vencida = models.CharField(max_length=1)
    class Meta:
        managed = False
        db_table = 'dri_dcl_jurada_periodo'

class DriEstudio(models.Model):
    id_estudioc = models.IntegerField(primary_key=True)
    denominacion = models.CharField(db_column='Denominacion', max_length=100) # Field name made lowercase.
    usuario = models.CharField(max_length=30, blank=True)
    clave = models.CharField(max_length=30, blank=True)
    numero = models.CharField(max_length=30)
    email = models.CharField(max_length=100, blank=True)
    class Meta:
        managed = False
        db_table = 'dri_estudio'

class DriEstudioPadron(models.Model):
    id_negocio = models.IntegerField(primary_key=True)
    id_estudioc = models.IntegerField(blank=True, null=True)
    id_padron = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dri_estudio_padron'

class DriPadronActividades(models.Model):
    id_padron = models.IntegerField()
    id_actividad = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    principal = models.CharField(max_length=1, blank=True)
    monto_minimo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    expediente = models.CharField(max_length=20, blank=True)
    id_sinc = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'dri_padron_actividades'

class DriPeriodos(models.Model):
    id_padron = models.IntegerField()
    id_actividad = models.IntegerField()
    anio = models.IntegerField()
    mes = models.IntegerField()
    base = models.DecimalField(max_digits=15, decimal_places=2)
    alicuota = models.DecimalField(max_digits=15, decimal_places=6)
    minimo = models.DecimalField(max_digits=15, decimal_places=2)
    impuesto = models.DecimalField(max_digits=15, decimal_places=2)
    detalle = models.CharField(max_length=30)
    class Meta:
        managed = False
        db_table = 'dri_periodos'

class Responsables(models.Model):
    id_responsable = models.IntegerField(primary_key=True)
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
        managed = False
        db_table = 'responsables'

class Sinc(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    ultimo_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sinc'

class SincLog(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    ultimo_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sinc_log'

class SincPers(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    ultimo_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sinc_pers'

class Tributo(models.Model):
    id_tributo = models.IntegerField(primary_key=True)
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
    class Meta:
        managed = False
        db_table = 'tributo'

class TributoInteres(models.Model):
    id_tributo = models.IntegerField(blank=True, null=True)
    desde = models.DateField(blank=True, null=True)
    hasta = models.DateField(blank=True, null=True)
    tipo_interes = models.IntegerField(blank=True, null=True)
    interes = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tributo_interes'

