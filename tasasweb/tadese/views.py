# -*- coding: utf-8 -*-

from django.template import Context
from django.shortcuts import *
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView
from django.conf import settings
from django.db.models import Count,Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.contrib import messages
from tadese.utilidades import *
from django import http
from django.http import Http404
import json
from datetime import datetime,date
from dateutil.relativedelta import *
from django.db.models import Q,F,Subquery
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

from tasasweb.views import volverHome,recargarLogueo
from .models import *

####################################################
# Funciones que utilizan varios procedimientos
####################################################

def getVariableConfig(variable,tipo):# pragma: no cover
    """Busca en la tabla configuracion_variables por una variable y devuelve el tipo determinado"""
    try:
        valor = None
        if variable:
            valor = Configuracion_vars.objects.get(variable=variable)
        if valor:
            if tipo=='numero':
                return valor.numero
            elif tipo=='texto':
                return valor.texto
            elif tipo=='fecha':
                return valor.fecha            
    except:
        return None

def getConfigVars():# pragma: no cover
    """Busca en la tabla configuracion_variables por una variable y devuelve su valor"""
    return {x.variable:{'texto':x.texto,'numero':x.numero,'fecha':x.fecha} for x in Configuracion_vars.objects.all()}

def dictfetchall(cursor):# pragma: no cover
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def padrones_x_estudio(id_estudioc):
    """Busca los padrondes de un estudio determinado"""    
    cursor = connection.cursor()
    cursor.execute("SELECT c.id_padron,c.padron,c.nombre as nombreResp,t.abreviatura as tipoTributo,count(c.id_padron) as cant_cuotas\
        FROM dri_estudio_padron dep \
        JOIN cuotas c on (c.id_padron=dep.id_padron) \
        JOIN tributo t on (c.tributo=t.id_tributo) \
        WHERE (dep.id_estudioc =  %s)and(t.id_tributo=6) GROUP BY c.id_padron,c.padron order by c.nombre,c.padron",[id_estudioc])
    padrones = dictfetchall(cursor)
    return padrones

def deuda_x_padron(idPadron,anio):
    """Busca la deuda de un padron determinado"""    
    cursor = connection.cursor()    
    if (anio>0):
        cursor.execute("SELECT c.*,db.id_boleta as boleta,db.pago_anterior as pago_anterior,db.minimo_global as minimo_global,\
                    db.total as total,db.fechapago,t.CORRER_VENC_DIAS,t.CORRER_VENC_FDESDE,t.CORRER_VENC_FHASTA \
                    FROM cuotas c LEFT JOIN dri_boleta db on (c.id_cuota=db.id_cuota) LEFT JOIN tributo t on (c.tributo=t.id_tributo) \
                    WHERE (c.id_padron = %s)and(c.anio = %s) order by c.anio DESC,CAST(TRIM(c.cuota) AS SIGNED) DESC,c.vencimiento DESC",[idPadron,anio])
    else:
        cursor.execute("SELECT c.*,db.id_boleta as boleta,db.pago_anterior as pago_anterior,db.minimo_global as minimo_global,\
                db.total as total,db.fechapago,t.CORRER_VENC_DIAS,t.CORRER_VENC_FDESDE,t.CORRER_VENC_FHASTA \
                FROM cuotas c LEFT JOIN dri_boleta db on (c.id_cuota=db.id_cuota) LEFT JOIN tributo t on (c.tributo=t.id_tributo) \
                WHERE c.id_padron = %s order by c.anio DESC,CAST(TRIM(c.cuota) AS SIGNED) DESC,c.vencimiento DESC",[idPadron])


    cuotas = dictfetchall(cursor)
    return cuotas

def padrones_x_responsable(idResp,idPadron=None):
    """Busca los padrondes de un responsable determinado"""    
    padrones = Cuotas.objects.filter(id_responsable=idResp).order_by('tributo','padron','id_padron').values('id_padron','padron','tributo','tributo__descripcion','tributo__abreviatura').annotate(Count('id_padron'))  
    if idPadron:
        padrones=padrones.filter(id_padron=idPadron)
    return padrones

def cuotas_x_padron(idResp,idPadron):
    """Busca las cuotas según un padrón determinado"""    
    if idResp is None:
        cuotas = Cuotas.objects.filter(id_padron=idPadron)
    else:
        cuotas = Cuotas.objects.filter(id_padron=idPadron,id_responsable=idResp)
    return cuotas

def puedeVerPadron(request,idPadron):
    """Según sea dueño del padrón o sea un estudio encargado del mismo continúa, sino lo vuela"""    
    try:        
        tipoUsr=request.user.userprofile.tipoUsr                
        
        if request.user.userprofile.id_estudioc==None:
                idEstudio=0
        else:
            idEstudio= int(request.user.userprofile.id_estudioc)       
        if tipoUsr==0:
            idr=int(request.user.userprofile.id_responsable)                       
            lista_resp = list(set(Cuotas.objects.filter(id_padron=idPadron).values_list('id_responsable', flat=True)))            
            lista = [int(x) for x in lista_resp]                                    
            if not(idr in lista):
                return volverHome(request)               
        elif tipoUsr==1:
            try:
                estudio = DriEstudioPadron.objects.filter(id_padron=int(idPadron)).values_list('id_estudioc',flat=True)
            except ObjectDoesNotExist:
                estudio = None   
                return volverHome(request)   

            
            if not (int(idEstudio) in estudio):
                return volverHome(request)        
    except:
        return volverHome(request)

class TienePermisoMixin(object):# pragma: no cover
    """Según sea dueño del padrón o sea un estudio encargado del mismo continúa, sino lo vuela"""    
    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().id_estudioc != self.request.user.userprofile.id_estudioc):
            raise http.Http404
        return super(TienePermisoMixin, self).dispatch(request, *args, **kwargs)

##############################################
#      Mixin para cargar las Vars de sistema #
##############################################
class VariablesMixin(object):
    """Variables de contexto para las Vistas (CBV)"""    
    def get_context_data(self, **kwargs):
        context = super(VariablesMixin, self).get_context_data(**kwargs)
        context['idMuni'] = settings.MUNI_ID
        context['dirMuni'] = settings.MUNI_DIR        
        context['DIR_MUNIS'] = settings.DIR_MUNIS
        puede_rectificar = 'N'
        try:
            sitio = Configuracion.objects.all().first()
            if sitio:
                puede_rectificar = sitio.puede_rectificar
        except Configuracion.DoesNotExist:
            return volverHome(request)             

        config = getConfigVars()
        context['sitio'] = sitio        
        context['puede_rectificar'] = puede_rectificar  == 'S'        
        context['fecha_hoy'] = date.today()        
        context['pago_online'] = config.get('pago_online', {}).get('texto','N') == 'S'
        context['suscripcion'] = sitio.suscripcion == 'S'
        context['suscripcion_msj'] = sitio.suscripcion_msj
        context['cartel_inicio'] = config.get('dri_cartel_inicio', {}).get('texto',None)
        return context

def getVariablesMixin(request):
    """Variables de contexto para las Funciones (FBV)"""    
    context = {} 
    context['idMuni'] = settings.MUNI_ID
    context['dirMuni'] = settings.MUNI_DIR                
    puede_rectificar = 'N'
    try:
        sitio = Configuracion.objects.all().first()
        if sitio:
            puede_rectificar = sitio.puede_rectificar
    except Configuracion.DoesNotExist:
        return volverHome(request)            
    config = getConfigVars()      
    context['sitio'] = sitio        
    context['puede_rectificar'] = puede_rectificar  == 'S'          
    context['fecha_hoy'] = date.today()                        
    context['pago_online'] = config.get('pago_online', {}).get('texto','N') == 'S'
    context['suscripcion'] = sitio.suscripcion == 'S'
    context['suscripcion_msj'] = sitio.suscripcion_msj    
    context['cartel_inicio'] = config.get('dri_cartel_inicio', {}).get('texto',None)
    context['DIR_MUNIS'] = settings.DIR_MUNIS
    return context

##############################################
#      Padrones de Estudios Contables        #
##############################################

class EstudiosView(VariablesMixin,TemplateView):
    """Vista que lista todos los padrones que tiene a cargo el estudio"""    
    template_name = 'padrones_estudio.html'
    context_object_name = 'estudios'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):        
        tipoUsr=self.request.user.userprofile.tipoUsr                        
        if tipoUsr<>1:
            return volverHome(self.request)
        return super(EstudiosView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EstudiosView, self).get_context_data(**kwargs)        
        
        try:
            idEst= int(self.request.user.userprofile.id_estudioc)
            estudio=DriEstudio.objects.get(id_estudioc=idEst)
        except:
            idEst=0
            estudio = None
            recargarLogueo(self.request)
        
        try:        
            context['estudio'] = estudio
            p = padrones_x_estudio(idEst)
            context['padr'] = p
            
            context['padron'] = p[0]
            
        except IndexError:
            context['padr'] = None
            context['padron'] = None
        return context

##########################################
#        Padrones de Responsables        #
##########################################
class PadronesView(VariablesMixin,TemplateView):
    """Vista que lista todos los padrones que tiene a cargo el Contribuyente"""    
    template_name = 'padrones_representante.html'
    context_object_name = 'padrones'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        tipoUsr=self.request.user.userprofile.tipoUsr  
        if tipoUsr<>0:
            return volverHome(self.request)
        return super(PadronesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PadronesView, self).get_context_data(**kwargs)                
        try:
            idResp= int(self.request.user.userprofile.id_responsable)
            p = padrones_x_responsable(idResp,None)            
            try:
                  sitio = Configuracion.objects.all().first()
            except Configuracion.DoesNotExist:
                  sitio = None
            if sitio <> None:
                if (sitio.ver_unico_padron == 'S'):
                 if "usuario" in self.request.session:
                    p = p.filter(padron=self.request.session["usuario"])
                    
            context['padr'] = p 
            context['padron'] = p[0]
        except:
            context['padr'] = None
            context['padron'] = None
            recargarLogueo(self.request)
        return context

##################################################
#      Ver cuotas del Padrón seleccionado        #
##################################################
class BusquedaCuotasView(VariablesMixin,TemplateView):
    """Vista que lista todos las cuotas de un padrón, sea filtradas por año o nó"""    
    template_name = 'cuotas2.html'
    context_object_name = 'cuotas'
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        idPadron = self.kwargs.get("idp",'0')       
        
        puedeVerPadron(self.request,idPadron)
        print "Cantidad de Queries:%s" % len(connection.queries)
        return super(BusquedaCuotasView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(BusquedaCuotasView, self).get_context_data(**kwargs)
        # En el contrxto pongo el padrón seleccionado asi saco sus características
        idPadron = self.kwargs.get("idp",'0')        
        anio = int(self.kwargs.get("anio",'0'))
        
        context['anio']=anio
        

        c = cuotas_x_padron(None,idPadron).order_by('-id_cuota').first()        
        idResp = c.id_responsable
        resp = c.get_responsable()       

        context['responsable'] = resp
        context['padr'] = padrones_x_responsable(idResp,None)        
        if idResp:
            if idPadron:
                try:
                    p = padrones_x_responsable(idResp,idPadron).first()
                except:
                    p = None
                context['padron']=p
        
        tributo=p['tributo']
        context['tributo'] = tributo
        
        c = Cuotas.objects.raw("SELECT c.*,db.id_boleta as boleta,db.pago_anterior as pago_anterior,db.minimo_global as minimo_global,\
                db.total as total,db.fechapago,t.CORRER_VENC_DIAS,t.CORRER_VENC_FDESDE,t.CORRER_VENC_FHASTA \
                FROM cuotas c LEFT JOIN dri_boleta db on (c.id_cuota=db.id_cuota) LEFT JOIN tributo t on (c.tributo=t.id_tributo) \
                WHERE c.id_padron = %s order by c.anio DESC,CAST(TRIM(c.cuota) AS SIGNED) DESC,c.vencimiento DESC",[idPadron])
            
        print c.query

        try:
            c = cuotas_x_padron(None,idPadron).order_by('-id_cuota').first()        
            idResp = c.id_responsable
            resp = c.get_responsable()       

            context['responsable'] = resp
            context['padr'] = padrones_x_responsable(idResp,None)        
            if idResp:
                if idPadron:
                    try:
                        p = padrones_x_responsable(idResp,idPadron).first()
                    except:
                        p = None
                    context['padron']=p
                    
            if (anio>0):                
                c = Cuotas.objects.raw("SELECT c.*,db.id_boleta as boleta,db.pago_anterior as pago_anterior,db.minimo_global as minimo_global,\
                    db.total as total,db.fechapago,t.CORRER_VENC_DIAS,t.CORRER_VENC_FDESDE,t.CORRER_VENC_FHASTA \
                    FROM cuotas c LEFT JOIN dri_boleta db on (c.id_cuota=db.id_cuota) LEFT JOIN tributo t on (c.tributo=t.id_tributo) \
                    WHERE (c.id_padron = %s)and(c.anio = %s) order by c.anio DESC,CAST(TRIM(c.cuota) AS SIGNED) DESC,c.vencimiento DESC",[idPadron,anio])
            else:
                c = Cuotas.objects.raw("SELECT c.*,db.id_boleta as boleta,db.pago_anterior as pago_anterior,db.minimo_global as minimo_global,\
                db.total as total,db.fechapago,t.CORRER_VENC_DIAS,t.CORRER_VENC_FDESDE,t.CORRER_VENC_FHASTA \
                FROM cuotas c LEFT JOIN dri_boleta db on (c.id_cuota=db.id_cuota) LEFT JOIN tributo t on (c.tributo=t.id_tributo) \
                WHERE c.id_padron = %s order by c.anio DESC,CAST(TRIM(c.cuota) AS SIGNED) DESC,c.vencimiento DESC",[idPadron])

            print c.model_fields
            
            

            context['cuotas'] = c
            context['cant_cuotas'] = len(list(c))
        except:
            context['responsable'] = None
            context['padr'] = None
            context['padron'] = None
            context['cuotas'] = None
            context['cant_cuotas'] = None

        context['suscriptor'] = get_suscriptor(idPadron)
        
        try:
            context['NoComercio'] = int(getConfigVars().get('NoComercio', {}).get('numero','0'))
            context['URL_CAJERO24'] = URL_CAJERO24        
            context['modif_bases_imp'] = getConfigVars().get('modif_bases_imp', {}).get('texto','N')=='S'            
        except:
            pass
        print "Cantidad de Queries:%s" % len(connection.queries)        
        return context


##########################################################################
def armarImgCodBar(cod):# pragma: no cover
    """Devuelve la imagen(PNG) del código de barras que se le pase(el texto)"""    
    import imprimirPDF
    b  = imprimirPDF.get_image3(cod)
    return b

def generarCodBar(idc,total1,total2,vencimiento,vencimiento2):
    """Devuelve el Codigo de Barras de 48/60 dígitos"""    
    try:
        c = Cuotas.objects.get(id_cuota=idc) 
    except:
        return None
    try:
        sitio = Configuracion.objects.all().first()
        diasExtra = sitio.diasextravencim
    except Configuracion.DoesNotExist:
        return None
   
    if diasExtra == None:
        diasExtra=0

    hoy = date.today()
    if (not vencimiento)and(not vencimiento2):
        vencimiento=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[0]
        vencimiento2=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[1]

        if (hoy >= c.vencimiento):
            vencimiento = hoy + relativedelta(days=diasExtra)   
            vencimiento2 = vencimiento
        else:
            vencimiento = c.vencimiento
            
        if c.segundo_vencimiento==None:
               vencimiento2 = vencimiento + relativedelta(months=1)
        elif (hoy <= c.segundo_vencimiento):
               vencimiento2 = c.segundo_vencimiento   
    try:
        longCB =sitio.longitudCodigoBarra
        if not sitio.longitudCodigoBarra:
            longCB = 48    
    except:
        longCB = 48
    
    try:               
        if (longCB==60)or((longCB<=60)and(float(total2)>=100000)):                    
            cod = generarCB60(sitio.id,c.tributo.id_tributo,vencimiento,total1,vencimiento2,total2,c.id_cuota,c.anio,c.cuota)            
        else:
            cod = generarCB48(sitio.id,c.tributo.id_tributo,vencimiento,total1,vencimiento2,total2,c.id_cuota,c.anio,c.cuota)
    except:
        return None    
    return cod


from easy_pdf.rendering import render_to_pdf_response

def imprimirPDF(request,idc,idb=None):       
    """Genera un PDF de la boleta a imprimir, sea la cuota o una DDJJ de DReI"""  
    from Code128 import Code128
    from base64 import b64encode
        
    try:
        c = Cuotas.objects.get(id_cuota=idc) 
    except:
        raise Http404
   
    puedeVerPadron(request,c.id_padron)       

    diasExtra = None
       
    try:
        sitio = Configuracion.objects.all().first()
        diasExtra = sitio.diasextravencim
    except Configuracion.DoesNotExist:
        raise Http404

    if diasExtra == None:
        diasExtra=0

    hoy = date.today()


    vencimiento=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[0]
    vencimiento2=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[1]


    if (hoy >= vencimiento):
        if ((hoy>vencimiento)and(hoy<=vencimiento2)):
            vencimiento = vencimiento2      
        else:
            vencimiento = hoy + relativedelta(days=diasExtra)  

    if (vencimiento2<=vencimiento):
           vencimiento2 = vencimiento            

    context = {}
    context = getVariablesMixin(request)  
    try:
        context['cuota'] = c    
        context['fecha'] = hoy
        context['vencimiento'] = vencimiento
        context['codseg'] = c.codseg    
    except:
        return volverHome(request)

    if c.tributo.id_tributo == 6 :
       template ='boletas/boleta_drei.html'
       
       if idb:
           boleta = DriBoleta.objects.filter(id_boleta=idb).first()
           context['titulo']=u'Boleta Rectificativa DReI'
       else:
           boleta = DriBoleta.objects.filter(id_cuota=c).first()
           context['titulo']=u'Boleta Liquidación DReI'
      
       a = DriBoleta_actividades.objects.filter(id_boleta=boleta)
      
       try:
           minimo_principal = DriPadronActividades.objects.filter(id_padron=boleta.id_padron,principal='S').aggregate(sum=Sum('monto_minimo'))['sum'] or 0
       except:
           minimo_principal = 0
       
       tot_adicionales =  boleta.derecho_neto + boleta.tasa_salud_publ + boleta.adic_monto + boleta.retenciones               
       totActiv = a.aggregate(sum=Sum('impuesto'))['sum'] or 0
       subtotal = totActiv + tot_adicionales
       recargo = boleta.recargo
       config = getConfigVars()  
       detalle_retenc = config.get('dri_retenciones', {}).get('texto','Devoluc/Retenc')
       context['detalle_retenc'] = detalle_retenc
       context['actividades'] = a
       context['cant_actividades'] = len(a)
       #Limito la cantidad de actividades a mostrar a 6 en el 2do y 3er cuerpo (por espacio)
       context['cant_actividades_restantes'] = len(a) - 6
         
       try:
            if boleta.minimo_global <= 0:
                # si es boleta vieja vencida le pongo el saldo de la cuota (minimo de ese momento)
                if (hoy > vencimiento):
                    context['minimo_principal'] = c.saldo
                else:
                    context['minimo_principal'] = minimo_principal
            else:
                context['minimo_principal'] = boleta.minimo_global            
       except:
            context['minimo_principal'] = minimo_principal
       
       if totActiv <= context['minimo_principal']:
            context['minimo_principal'] = totActiv

       context['totActiv'] = totActiv
       context['boleta'] = boleta
       context['recargo'] = recargo
       context['subtotal'] = subtotal     
       context['tot_adicionales'] = tot_adicionales
       context['vencimiento2'] = vencimiento
       vencimiento2 = vencimiento      
       total1 = Decimal(boleta.total)   
       total2 = Decimal(boleta.total)       
    else:
       template = 'boletas/boleta_tasas.html'
       totales  = calcularPunitorios(request,c,None,0)       
       context['vencimiento2'] = vencimiento2
       total1 = totales['punit1']
       context['porc1'] = totales['porc1']
       total2 = totales['punit2']
       context['porc2'] = totales['porc2']  
    
    if ((sitio.codigo_link_visible=='S') or (sitio.codigo_link_visible=='')):
        context['codLINK'] = str(c.id_padron).rjust(9, "0")
    else:
        context['codLINK'] = ''
    
    context['punit1'] = total1      
    context['punit2'] = total2          
    
    cod=generarCodBar(idc,total1,total2,vencimiento,vencimiento2)

    try:
        longCB =sitio.longitudCodigoBarra
        if not sitio.longitudCodigoBarra:
            longCB = 48    
    except:
        longCB = 48

    leyenda = None

    if (longCB<60)and(float(total2)>=100000):        
        leyenda = u"La presente boleta deberá ser abonada únicamente en el Municipio."

    context['leyenda'] = leyenda
    context['codbar'] = armarImgCodBar(cod)
    cod = " ".join(cod[i:i+5] for i in range(0, len(cod), 5)).replace(' ', ' ')
    context['codigo'] = cod
    
    return render_to_pdf_response(request, template, context)

##################################################
#     Liquidacion DReI                         #
##################################################
from django.forms.models import inlineformset_factory
from .forms import LiqDreiBoletaForm,LiqDreiActivForm,EstudioForm,ResponsableForm,BusquedaDDJJForm,LiqDreiRectifForm,LiqDreiBasesForm
from django.db import transaction
from django.contrib.messages import constants as message_constants

class DreiLiquidarCreateView(VariablesMixin,CreateView):
    """Genera una boleta de DReI""" 
    form_class = LiqDreiBoletaForm
    template_name = 'drei/drei_liquidacion.html'     
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                   
        return super(DreiLiquidarCreateView, self).dispatch(*args, **kwargs)
    
    def get_initial(self):    
        initial = super(DreiLiquidarCreateView, self).get_initial()                        
        return initial   

    def get_form_kwargs(self,**kwargs):
        kwargs = super(DreiLiquidarCreateView, self).get_form_kwargs()        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DreiLiquidarCreateView, self).get_context_data(**kwargs)
        idc = int(self.kwargs.get("idc",'0'))                
        try:
            cuota = Cuotas.objects.get(id_cuota=idc)                 
            sitio = Configuracion.objects.all().first()
        except:            
            return volverHome(request)    
        
        if cuota:            
            context['cuota'] = cuota                   
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        
        context['titulo'] = u'Autoliquidación de Boletas de DReI'       
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        context = self.get_context_data()
        idc = int(self.kwargs.get("idc",'0'))        
        cuota = Cuotas.objects.get(id_cuota=idc)    
        if not cuota:
            return volverHome(request)
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return volverHome(request)
        minGlobal=0
        minimo = 0
        hoy = date.today()        
        actividades = DriCuotaActividad.objects.filter(id_cuota=cuota)
        #Si no existe la cuota, busco la cuota más nueva que exista del mismo padrón y traigo sus actividades
        if not actividades:           
            try:
                cc = DriCuotaActividad.objects.filter(id_padron=cuota.id_padron).order_by('-id_cuota').first().id_cuota
                actividades = DriCuotaActividad.objects.filter(id_cuota=cc)
            except:
                messages.add_message(self.request, messages.ERROR,u'Verifique que las Actividades estén cargadas correctamente!.')
                return volverHome(request)
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)
        data_activ = []
        if actividades.count()>0:
            for activ in actividades:
                if activ.minimo is None:
                    minimo = 0
                if activ.actividad_principal != 'S':
                    minimo = 0
                else:
                    if sitio.minimo_por_activ=='S':
                       minimo = activ.minimo
                
                    minGlobal+=minimo

                if activ.alicuota is None:
                    alicuota = 0
                else:
                    alicuota = activ.alicuota
           
                data_activ.append({'id_actividad': activ.id_actividad,'minimo':minimo,'alicuota':alicuota,'activ_descr':activ.get_actividad(),'base':'0','impuesto':'0'})
                        
        if sitio:
            if (sitio.minimo_por_activ=='N'):
                minGlobal=cuota.saldo
        
        data = {'id_padron': cuota.id_padron,'anio': cuota.anio,'mes': cuota.cuota,'vencimiento': cuota.vencimiento,'total':0,
                    'recargo':0,'derecho_neto':0,'tasa_salud_publ':0,'retenciones':0,'adic_monto':0,'id_cuota':cuota.id_cuota,'minimo_global':minGlobal}

        form = LiqDreiBoletaForm(initial=data)
        actividades_formset = ActividadesFormSet(instance=DriBoleta(),prefix='actividades',initial=data_activ)       
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset,minimo_global=minGlobal))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',can_delete=False,form=LiqDreiActivForm)     
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades')        
                
        if form.is_valid() and actividades_formset.is_valid():            
            return self.form_valid(form, actividades_formset)
        else:
            return self.form_invalid(form, actividades_formset)        

    def form_valid(self, form, actividades_formset):
        self.object = form.save(commit=False)        
        context = self.get_context_data()
        idc = int(self.kwargs.get("idc",'0'))        
        cuota = Cuotas.objects.get(id_cuota=idc)    
        # cuota = context['cuota']
        hoy = date.today()       
        self.object.id_cuota = cuota
        self.object.save()       
        actividades_formset.instance = self.object       
        actividades_formset.save()                                
        return super(DreiLiquidarCreateView, self).form_valid(form)
    
    def get_success_url(self):
        idc = int(self.kwargs.get("idc",'0'))
        cuota = Cuotas.objects.get(id_cuota=idc)  
        messages.add_message(self.request, messages.SUCCESS,u'El Período %s/%s fué liquidado exitosamente!. Recuerde Imprimir la Boleta.' % (cuota.cuota,cuota.anio))
        return reverse('ver_cuotas', kwargs={'idp':cuota.id_padron})

    def form_invalid(self, form,actividades_formset):                                                       
        context = self.get_context_data()
        cuota = context['cuota']
        hoy = date.today()       
        actividades = DriCuotaActividad.objects.filter(id_cuota=cuota)
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)        
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades')
        minimo = form.cleaned_data['minimo_global']    
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

class DreiLiquidarUpdateView(VariablesMixin,UpdateView):
    """Edita una boleta de DReI""" 
    form_class = LiqDreiBoletaForm
    template_name = 'drei/drei_liquidacion.html' 
    model = DriBoleta
    pk_url_kwarg = 'idb'
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                   
        return super(DreiLiquidarUpdateView, self).dispatch(*args, **kwargs)
    
    def get_initial(self):    
        initial = super(DreiLiquidarUpdateView, self).get_initial()                        
        return initial   

    def get_form_kwargs(self,**kwargs):
        kwargs = super(DreiLiquidarUpdateView, self).get_form_kwargs()        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DreiLiquidarUpdateView, self).get_context_data(**kwargs)
        idb = int(self.kwargs.get("idb",'0'))        
        boleta = DriBoleta.objects.get(id_boleta=idb)
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if boleta:
            cuota = boleta.id_cuota            
            context['cuota'] = cuota            
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        context['titulo'] = u'Reliquidar Boleta de DReI'       
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        
        boleta = self.object        
        
        
        if boleta:
            cuota = boleta.id_cuota
            hoy = date.today()                         
            boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta)                        
            maximo=len(boleta_activ)            
            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=maximo,max_num=maximo,can_delete=False,form=LiqDreiActivForm)                    
            data_activ = []
            minGlobal=0
            minimo = 0
            for activ in boleta_activ:
                    data_activ.append({'id_actividad':activ.id_actividad,'activ_descr':activ.activ_descr,'base':activ.base,'alicuota':activ.alicuota,'minimo':activ.minimo,'impuesto':activ.impuesto})                                                      
            minGlobal=boleta.minimo_global
            if sitio:
                if (sitio.minimo_por_activ=='N'):
                    minGlobal=cuota.saldo
                        
            data = {'minimo_global':minGlobal}

            form = LiqDreiBoletaForm(instance=boleta,initial=data)
            if boleta.adic_detalle:
                try: 
                    adic = [item for item in ADICIONALES if item[1] == boleta.adic_detalle]           
                    form.fields['adic_select'].initial = int(adic[0][0])
                except:
                    pass
            
            actividades_formset = ActividadesFormSet(prefix='actividades',instance=boleta,initial=data_activ)     
        else:
            return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

    def post(self, request, *args, **kwargs):        
        self.object = self.get_object()
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        boleta = self.object                   
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',can_delete=False,form=LiqDreiActivForm)     
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades',instance=boleta)        
        if form.is_valid() and actividades_formset.is_valid():            
            return self.form_valid(form, actividades_formset)
        else:
            return self.form_invalid(form, actividades_formset)        

    def form_valid(self, form, actividades_formset):
        self.object = form.save(commit=False)        
        context = self.get_context_data()
        cuota = context['cuota']
        self.object.id_cuota = cuota
        self.object.save()             
        actividades_formset.instance = self.object       
        actividades_formset.save()                                
        return super(DreiLiquidarUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        idb = int(self.kwargs.get("idb",'0'))
        boleta = DriBoleta.objects.get(id_boleta=idb)
        cuota = boleta.id_cuota
        messages.add_message(self.request, messages.SUCCESS,u'El Período %s/%s fué Reliquidado exitosamente!. Recuerde Imprimir la Boleta.' % (cuota.cuota,cuota.anio))
        return reverse('ver_cuotas', kwargs={'idp':boleta.id_cuota.id_padron})

    def form_invalid(self, form,actividades_formset):                                                       
        boleta = self.get_object()                          
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',can_delete=False,form=LiqDreiActivForm)  
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades',instance=boleta)        
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

#################################################################

class DreiRectificarNew(VariablesMixin,CreateView):
    """Genera una boleta de Rectificación DReI a partir de una Cuota""" 
    form_class = LiqDreiRectifForm
    template_name = 'drei/drei_liquidacion.html'     
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                   
        return super(DreiRectificarNew, self).dispatch(*args, **kwargs)
    
    def get_initial(self):    
        initial = super(DreiRectificarNew, self).get_initial()                        
        return initial   

    def get_form_kwargs(self,**kwargs):
        kwargs = super(DreiRectificarNew, self).get_form_kwargs()        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DreiRectificarNew, self).get_context_data(**kwargs)
        idc = int(self.kwargs.get("idc",'0'))        
        cuota = Cuotas.objects.get(id_cuota=idc)          
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if cuota:            
            context['cuota'] = cuota                    
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        context['titulo'] = u'Rectificativa de Boletas de DReI'       
        context['rectificativa'] = True
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        context = self.get_context_data()
        idc = int(self.kwargs.get("idc",'0'))        
        cuota = Cuotas.objects.get(id_cuota=idc)    
        # cuota = context['cuota']    
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        minGlobal=0
        minimo = 0
        hoy = date.today()        
        actividades = DriCuotaActividad.objects.filter(id_cuota=cuota)
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)
        data_activ = []
        if actividades.count()>0:
            for activ in actividades:
                if activ.minimo is None:
                    minimo = 0
                if activ.actividad_principal != 'S':
                    minimo = 0
                else:
                    if sitio.minimo_por_activ=='S':
                       minimo = activ.minimo
                
                    minGlobal+=minimo

                if activ.alicuota is None:
                    alicuota = 0
                else:
                    alicuota = activ.alicuota
           
                data_activ.append({'id_actividad': activ.id_actividad,'minimo':minimo,'alicuota':alicuota,'activ_descr':activ.denominacion,'base':'0','impuesto':'0'})
                        
        if sitio:
            if (sitio.minimo_por_activ=='N'):
                minGlobal=cuota.saldo
        
        data = {'id_padron': cuota.id_padron,'anio': cuota.anio,'mes': cuota.cuota,'vencimiento': cuota.vencimiento,'total':0,
                    'recargo':0,'derecho_neto':0,'tasa_salud_publ':0,'retenciones':0,'adic_monto':0,'id_cuota':cuota.id_cuota,'minimo_global':minGlobal}

        form = LiqDreiRectifForm(initial=data)
        actividades_formset = ActividadesFormSet(instance=DriBoleta(),prefix='actividades',initial=data_activ)       
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',can_delete=False,form=LiqDreiActivForm)     
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades')        
                
        if form.is_valid() and actividades_formset.is_valid():            
            return self.form_valid(form, actividades_formset)
        else:
            return self.form_invalid(form, actividades_formset)        

    def form_valid(self, form, actividades_formset):
        self.object = form.save(commit=False)        
        context = self.get_context_data()
        # cuota = context['cuota']
        idc = int(self.kwargs.get("idc",'0'))        
        cuota = Cuotas.objects.get(id_cuota=idc)    
        hoy = date.today()       
        self.object.id_cuota = cuota
        self.object.save()       
        actividades_formset.instance = self.object       
        actividades_formset.save()                                
        return super(DreiRectificarNew, self).form_valid(form)
    
    def get_success_url(self):
        idc = int(self.kwargs.get("idc",'0'))
        cuota = Cuotas.objects.get(id_cuota=idc)  
        messages.add_message(self.request, messages.SUCCESS,u'El Período %s/%s fué Rectificado exitosamente!. Recuerde Imprimir la Boleta.' % (cuota.cuota,cuota.anio))
        return reverse('ver_cuotas', kwargs={'idp':cuota.id_padron})

    def form_invalid(self, form,actividades_formset):                                                       
        
        context = self.get_context_data()
        # cuota = context['cuota']
        idc = int(self.kwargs.get("idc",'0'))        
        cuota = Cuotas.objects.get(id_cuota=idc)    
        hoy = date.today()       
        actividades = DriCuotaActividad.objects.filter(id_cuota=cuota)
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)        
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades')
            
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

class DreiRectificar(VariablesMixin,CreateView):
    """Genera una boleta de Rectificación DReI a partir de una Boleta""" 
    form_class = LiqDreiRectifForm
    template_name = 'drei/drei_liquidacion.html' 
    model = DriBoleta
    pk_url_kwarg = 'idb'
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                   
        return super(DreiRectificar, self).dispatch(*args, **kwargs)
    
    def get_initial(self):    
        initial = super(DreiRectificar, self).get_initial()                        
        return initial   

    def get_form_kwargs(self,**kwargs):
        kwargs = super(DreiRectificar, self).get_form_kwargs()        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DreiRectificar, self).get_context_data(**kwargs)
        idb = int(self.kwargs.get("idb",'0'))        
        boleta = DriBoleta.objects.get(id_boleta=idb)
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if boleta:
            cuota = boleta.id_cuota            
            context['cuota'] = cuota                    
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        context['rectificativa'] = True
        context['titulo'] = u'Rectificativa de Boletas de DReI'       
        return context

    def get(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        boleta =  self.object      
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')  
        if boleta:
            cuota = boleta.id_cuota
            hoy = date.today()             
            actividades = DriCuotaActividad.objects.filter(id_cuota=cuota)
            dria = actividades.values_list('id_actividad',flat=True)        
            #Borro las actividades preexistentes
            #boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta).delete()                        
            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=len(dria),can_delete=False,form=LiqDreiActivForm)                    
            data_activ = []
            minimo = 0
            alicuota = 0
            #cargo las actividades como que fuese una boleta nueva
            if actividades.count()>0:
                for activ in actividades:
                    if activ.minimo is None:
                        minimo = 0
                    if activ.actividad_principal != 'S':
                        minimo = 0
                    else:
                        if sitio.minimo_por_activ=='S':
                           minimo = activ.minimo

                    if activ.alicuota is None:
                        alicuota = 0
                    else:
                        alicuota = activ.alicuota
               
                    data_activ.append({'id_actividad': activ.id_actividad,'minimo':minimo,'alicuota':alicuota,'activ_descr':activ,'base':'0','impuesto':'0'})

            
            data = {'id_padron': boleta.id_padron,'anio': boleta.anio,'mes': boleta.mes,'vencimiento': boleta.vencimiento,'total':boleta.total,
                        'recargo':0,'derecho_neto':0,'tasa_salud_publ':0,'retenciones':0,
                        'adic_monto':0,'id_cuota':boleta.id_cuota,'minimo_global':boleta.minimo_global}

            form= LiqDreiRectifForm(initial=data)  
            actividades_formset = ActividadesFormSet(prefix='actividades',initial=data_activ)     
       
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

    def post(self, request, *args, **kwargs):
        
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',can_delete=False,form=LiqDreiActivForm)     
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades')        
                
        if form.is_valid() and actividades_formset.is_valid():            
            return self.form_valid(form, actividades_formset)
        else:
            return self.form_invalid(form, actividades_formset)        

    def form_valid(self, form, actividades_formset):
        self.object = form.save(commit=False)        
        context = self.get_context_data()
        cuota = context['cuota']
        self.object.id_cuota = cuota
        self.object.save()         
        actividades_formset.instance = self.object       
        actividades_formset.save()                                
        return super(DreiRectificar, self).form_valid(form)
    
    def get_success_url(self):
        idb = int(self.kwargs.get("idb",'0'))
        boleta = DriBoleta.objects.get(id_boleta=idb)
        messages.add_message(self.request, messages.SUCCESS,u'El Período %s/%s fué Rectificado exitosamente!. Recuerde Imprimir la Boleta.' % (boleta.id_cuota.cuota,boleta.id_cuota.anio))
        return reverse('ver_cuotas', kwargs={'idp':boleta.id_cuota.id_padron})

    def form_invalid(self, form,actividades_formset):                                                       
        boleta = self.get_object()          
        if boleta:
            cuota = boleta.id_cuota
            boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta)

            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=boleta_activ.count(),can_delete=False,form=LiqDreiActivForm)                    
            data_activ = []
            for activ in boleta_activ:                
                if activ:
                    data_activ.append({'id_actividad':activ.id_actividad,'activ_descr':activ})                
            actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades',initial=data_activ)
            
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

class DreiModifBasesView(VariablesMixin,UpdateView):
    """Modifica las Bases Imponibles de una Boleta ya liquidada y pagada""" 
    form_class = LiqDreiBoletaForm
    template_name = 'drei/drei_modif_bases.html' 
    model = DriBoleta
    pk_url_kwarg = 'idb'
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                   
        return super(DreiModifBasesView, self).dispatch(*args, **kwargs)
    
    def get_initial(self):    
        initial = super(DreiModifBasesView, self).get_initial()                        
        return initial   

    def get_form_kwargs(self,**kwargs):
        kwargs = super(DreiModifBasesView, self).get_form_kwargs()        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DreiModifBasesView, self).get_context_data(**kwargs)
        idb = int(self.kwargs.get("idb",'0'))        
        boleta = DriBoleta.objects.get(id_boleta=idb)
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if boleta:
            cuota = boleta.id_cuota            
            context['cuota'] = cuota            
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        context['titulo'] = u'Modificación Bases Imponibles'       
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        try:
            sitio = Configuracion.objects.all().first()
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        
        boleta = self.object        
                
        if boleta:
            cuota = boleta.id_cuota
            hoy = date.today()                         
            boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta)            
            maximo=len(boleta_activ)
            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=maximo,max_num=maximo,can_delete=False,form=LiqDreiBasesForm)                    
            data_activ = []            
            for activ in boleta_activ:                
                try:                                            
                    data_activ.append({'id_actividad':activ.id_actividad,'activ_descr':activ,'base':activ.base,'alicuota':activ.alicuota,'minimo':activ.minimo,'impuesto':activ.impuesto})                            
                except:                    
                    pass            
            minGlobal=boleta.minimo_global            
            data = {'minimo_global':minGlobal}
            form = LiqDreiBoletaForm(instance=boleta,initial=data)          
            actividades_formset = ActividadesFormSet(prefix='actividades',instance=boleta,initial=data_activ)     
        else:
            return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

    def post(self, request, *args, **kwargs):        
        self.object = self.get_object()
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        boleta = self.object           
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',can_delete=False,form=LiqDreiBasesForm)     
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades',instance=boleta)        
        if form.is_valid() and actividades_formset.is_valid():            
            return self.form_valid(form, actividades_formset)
        else:                       
            return self.form_invalid(form, actividades_formset)        

    def form_valid(self, form, actividades_formset):
        self.object = form.save(commit=False)        
        context = self.get_context_data()
        cuota = context['cuota']
        self.object.id_cuota = cuota
        self.object.save()        
        actividades_formset.instance = self.object       
        actividades_formset.save()                                
        return super(DreiModifBasesView, self).form_valid(form)
    
    def get_success_url(self):
        idb = int(self.kwargs.get("idb",'0'))
        boleta = DriBoleta.objects.get(id_boleta=idb)
        cuota = boleta.id_cuota
        messages.add_message(self.request, messages.SUCCESS,u'Las Bases Imponibles del Período %s/%s fueron modificadas exitosamente!. Recuerde ingresar la diferencia en negativo en el próximo Período(Devoluc/Retenc).' % (cuota.cuota,cuota.anio))
        return reverse('ver_cuotas', kwargs={'idp':boleta.id_cuota.id_padron})

    def form_invalid(self, form,actividades_formset):                                                       
        boleta = self.get_object()                  
        if boleta:
            hoy = date.today()
            cuota = boleta.id_cuota
            boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta)            
            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=len(boleta_activ),can_delete=False,form=LiqDreiBasesForm)                    
            data_activ = []
            for activ in boleta_activ:                
                if activ:
                    data_activ.append({'id_actividad':activ.id_actividad,'activ_descr':activ,'impuesto':activ.impuesto})                
            actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades',initial=data_activ)
        else:
            return HttpResponseRedirect('/')            
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

##################################################
#      Ver DDJJ LISTADOS                      #
##################################################
class DreiDDJJAList(VariablesMixin,ListView):
    """Listado de DDJJ realizadas por anio y padrón determinado (MUNICIPIOS)""" 
    template_name = 'drei/drei_ddjj_listado.html'
    context_object_name = 'ddjj'
    
    def dispatch(self, *args, **kwargs):
        anio = int(self.kwargs.get("anio",'0'))
        idPadron = self.kwargs.get("idp",'0')       
        puedeVerPadron(self.request,idPadron)
        return super(DreiDDJJAList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        idPadron = self.kwargs.get("idp",'0')
        anio = int(self.kwargs.get("anio",'0'))
        ddjj = DriBoleta.objects.filter(id_padron=idPadron)
        if (anio>0):
            ddjj = ddjj.filter(anio=anio)
            
        return ddjj

    def get_context_data(self, **kwargs):
        context = super(DreiDDJJAList, self).get_context_data(**kwargs)
        
        idPadron = self.kwargs.get("idp",'0')
        c = cuotas_x_padron(None,idPadron).order_by('-id_cuota').first()
        idResp = c.id_responsable
        anio = int(self.kwargs.get("anio",'0'))
        context['anio']=anio
        context['responsable'] = c.get_responsable()
        context['padr'] = padrones_x_responsable(idResp,None)        
        if idResp:
            if idPadron:
                try:
                    p = padrones_x_responsable(idResp,idPadron).first()
                except IndexError:
                    p = None
                context['padron']=p
        return context

##################################################
#      Update de Estudios                        #
##################################################
class EstudiosUpdateView(VariablesMixin,TienePermisoMixin,UpdateView):
    """Edición de datos del Estudio contable (password y correo)""" 
    template_name = 'estudio_update.html'
    model = DriEstudio
    success_url = '/'
    form_class = EstudioForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):        
        return super(EstudiosUpdateView, self).dispatch(*args, **kwargs)

####################################################

def mandarEmailEstudio(request,usrEstudio):
    """Envía un EMAIL con el usuario y contraseña del estudio (para recordatorio)"""     
    from django.core.mail import EmailMessage
    from django.core.mail.backends.smtp import EmailBackend    
    if request.is_ajax():
        message=''                
        try:
            estudio = DriEstudio.objects.filter(usuario=usrEstudio)[0]          
        except:            
            estudio = None            
            message = "El usuario es incorrecto."                        
            return HttpResponse(message)
               
        login_valid = (estudio <> None)
        
        if login_valid:
            to_addr=estudio.email
            if (to_addr=='')or(to_addr==None):
                return HttpResponse(u'El estudio no tiene asignada una dirección de e-mail. Por favor verifique.')
            clave = estudio.clave
            
            from_addr = 'contacto@grupoguadalupe.com.ar'
            msg = u'Ud. ha solicitado el envio de su password por email.\nSu password es: %s' % clave

            m = msg

            mail_cuerpo = m
            mail_servidor = settings.EMAIL_HOST
            mail_usuario = settings.EMAIL_HOST_USER
            mail_password = settings.EMAIL_HOST_PASSWORD
            mail_origen = from_addr

            asunto = u'Password Requerido Estudio Contable (Sistema Liquidacion OnLine)'
            
            if settings.TESTING:                
                from django.core.mail.backends.locmem import EmailBackend                
                mail_servidor = 'localhost'
            
            backend = EmailBackend(host=mail_servidor, username=mail_usuario,password=mail_password,fail_silently=False)        
            email = EmailMessage( subject=asunto,body=mail_cuerpo,from_email=mail_origen,to=[to_addr],connection=backend)                
            email.send()                  
            message=unicode("¡El e-mail fué enviado con éxito!", 'utf-8')
        return HttpResponse(message)
    else:
        return HttpResponse(unicode("ERROR sólo AJAX", 'utf-8'))

##########################################################################
# Funciones ajax para la liquidacion y cálculo de Punitorios ONLINE
##########################################################################

from .punitorios import punitorios
def calcularPunitorios(request,c,boleta=None,importe=0):
    # try:
        cuota = c       
        hoy = date.today()  
        vencimiento = cuota.vencimiento
        vencimiento2 = cuota.segundo_vencimiento
        nobonificable = cuota.tributo.nobonificable
        if not nobonificable:
            nobonificable = 0
        bonificable = cuota.tributo.bonificacion
        if (not bonificable)or(bonificable<0):
            bonificable = 0

        if vencimiento2==None:
           vencimiento2 = vencimiento
       

        fecha = hoy  
        
        vencimiento=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[0]
        vencimiento2=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[1]
               
        if cuota.tributo.id_tributo==6 :
            if cuota.segundo_vencimiento==None:
               vencimiento2 = vencimiento
            else:
               vencimiento2 = cuota.segundo_vencimiento 

            if boleta:
                if vencimiento <= boleta.fechapago:
                    vencimiento = boleta.fechapago
                if vencimiento2 <= boleta.fechapago:
                    vencimiento2 = boleta.fechapago

            if (hoy<=vencimiento):
                fecha=vencimiento                          
            elif (hoy>vencimiento):
                fecha=vencimiento2
            elif (hoy<=vencimiento2):
                fecha=vencimiento2
            else:
                fecha=hoy                                
                        
            porc1 = punitorios(cuota,fecha,importe)
            importe1 =  importe + porc1
            punit1 = importe1
            porc2 = porc1
            importe2 =  importe + porc2
            punit2 = importe2
            
        
        else:
            
                                     
            if (hoy<=vencimiento):
                fecha=vencimiento 
            elif ((hoy>vencimiento)and(hoy<=vencimiento2)):
                bonificable = 0
                nobonificable = 0
                fecha=vencimiento2
            else:
                fecha=hoy
                vencimiento2=fecha
                bonificable = 0
                nobonificable = 0
            
            #si no está vecida
            if (hoy<=vencimiento):                
                porc1 = Decimal(0).quantize(Decimal("0.01"))
            else:
                porc1 = punitorios(cuota,fecha,None)
            
            importe = (cuota.saldo - nobonificable) * (1-(bonificable/100)) + nobonificable            
            importe1 =  importe + porc1
            punit1 = importe1        

            if cuota.tributo.interes_2ven==0:                
                porc2 = porc1
            else:                
                porc2 = punitorios(cuota,vencimiento2,None)
            importe = cuota.saldo
            importe2 = importe + porc2
            punit2 = importe2                                

    # except Exception as e:
    #     print e.message        
    #     return HttpResponse('Error') # Error Manejado
        #if settings.DEBUG:
        #    print 'por1:'+str(importe1)+' porc1:'+str(porc1)+' punit1:'+str(punit1)+' por2:'+str(importe2)+' porc2:'+str(porc2)+' punit2:'+str(punit2)
        return {'punit1': format(punit1, '.2f'), 'porc1': format(porc1, '.2f'),'punit2': format(punit2, '.2f'), 'porc2': format(porc2, '.2f')}

@login_required
def generarPunitoriosLiq(request):   
    """Calcula y devuelve intereses de la liquidacion(conjunto de cuotas) que se está liquidando en pantalla(AJAX)""" 
    if request.is_ajax():         
            datos = request.GET.getlist('cuotas[]')            
            
            cuotasAct = {}            
            if datos:
                for i in datos:
                    c = Cuotas.objects.get(id_cuota=i) 
                    if c.tributo.id_tributo==6:
                        boleta = DriBoleta.objects.filter(id_padron=c.id_padron,anio=c.anio,mes=c.cuota).first()
                        total  = calcularPunitorios(request,c,boleta,boleta.total)                        
                    else:
                        total  = calcularPunitorios(request,c,None,0)
                    cuotasAct[i]=total['punit1']                    
                    
                    # subtotal = subtotal + float(totales['punit1'])
            return HttpResponse(json.dumps(cuotasAct), content_type = "application/json")

@login_required
def generarLiquidacion(request,idp):   
    """Calcula y genera una Liquidación (conjunto de cuotas) con tributo 998""" 
    if request.is_ajax():         
            padr = cuotas_x_padron(None,idp).first()
            id_unidad = padr.id_unidad
            datos = request.GET.getlist('cuotas[]')            
            subtotal = 0
            totNom = 0
            totInt = 0
            totales = {}
            if datos:
                for i in datos:
                    c = Cuotas.objects.get(id_cuota=i)                    
                    if c.tributo.id_tributo==6:
                        boleta = DriBoleta.objects.filter(id_padron=c.id_padron,anio=c.anio,mes=c.cuota).first()
                        
                        total  = calcularPunitorios(request,c,boleta,boleta.total)
                    else:
                        total  = calcularPunitorios(request,c,None,0)
                    totales[i]=total                    
                    totInt += float(total['porc1'])
                    totNom += float(total['punit1']) - float(total['porc1'])
                    subtotal += float(total['punit1'])
                # Genero la liquidacion    
                try:
                    sitio = Configuracion.objects.all().first()
                    diasExtra = sitio.diasextravencim
                except:
                    diasExtra = 0

                if diasExtra == None:
                    diasExtra=0
                hoy = date.today() 
                
                venc = hoy + relativedelta(days=diasExtra)   
                liq =WEB_Liquidacion(id_unidad = id_unidad,tipo=1,vencimiento=venc,nominal=totNom,interes = totInt,total = subtotal,\
                    pasado_a_cnv=0,usuario=request.user.username,fecha_punitorios = hoy,punitorios = totInt)
                liq.save()
                for i in datos:
                    c = Cuotas.objects.get(id_cuota=i)  
                    totNom = float(totales[i]['punit1']) - float(totales[i]['porc1'])
                    totInt = float(totales[i]['porc1'])
                    liq_cta = WEB_Liquidacion_ctas(id_liquidacion = liq,id_cuota=c,tributo=c.tributo.id_tributo,nominal=totNom ,interes=totInt)
                    liq_cta.save()
                if liq:                   
                    messages.add_message(request, messages.SUCCESS,u'Se generó con éxito la Liquidación Nº %s!.'  % (liq.pk))           
                    return HttpResponse(json.dumps(liq.id_liquidacion), content_type = "application/json")
                else:
                    return HttpResponse(json.dumps(None), content_type = "application/json")

@login_required
def imprimirPDFLiqWeb(request,id_liquidacion):   
    """Imprimo la liquidacion(conjunto de cuotas)""" 
    from Code128 import Code128
    from base64 import b64encode
        
    liq = WEB_Liquidacion.objects.get(id_liquidacion=id_liquidacion)    
    liq_ctas = WEB_Liquidacion_ctas.objects.filter(id_liquidacion=id_liquidacion).extra(
                        select = {'total': '(nominal + interes)'},).order_by('-id_cuota')
    
    descrCtas =''                        
    for i in liq_ctas:
        if descrCtas=='':
            descrCtas=(i.id_cuota.cuota+'/'+str(i.id_cuota.anio))
        else:
            descrCtas= descrCtas+' - ' +(i.id_cuota.cuota+'/'+str(i.id_cuota.anio))

    if liq_ctas:
        c = Cuotas.objects.get(id_cuota=liq_ctas.first().id_cuota.id_cuota)


    diasExtra = None
    try:
        sitio = Configuracion.objects.all().first()
        diasExtra = sitio.diasextravencim

    except Configuracion.DoesNotExist:
        sitio = None
        return HttpResponseRedirect(LOGIN_URL)
        
    if diasExtra == None:
        diasExtra=0

    hoy = date.today()

    vencimiento = liq.vencimiento
    vencimiento2 = vencimiento
 
    context = {}  
    context['liq'] = liq
    context['idMuni'] = settings.MUNI_ID
    context['dirMuni'] = settings.MUNI_DIR
    context['vencimiento'] = vencimiento   
    context['sitio'] = sitio
    context['cuota'] = c
    context['descrCtas'] = descrCtas
    
    from easy_pdf.rendering import render_to_pdf_response   
 
    template ='boletas/boleta_liq.html'
    context['liq_ctas'] = liq_ctas
    context['vencimiento2'] = vencimiento2

    try:
        longCB =sitio.longitudCodigoBarra
        if not sitio.longitudCodigoBarra:
            longCB = 48    
    except:
        longCB = 48

    leyenda = None
    
    if (longCB<60)and(liq.total>=100000):        
        leyenda = u"La presente boleta deberá ser abonada únicamente en el Municipio."

    context['leyenda'] = leyenda

    try:
        cod = generarCB48(sitio.id,'998',vencimiento,liq.total,vencimiento2,liq.total,liq.id_liquidacion,liq.fecha.year,liq.fecha.month)
    
        if sitio.longitudCodigoBarra==60:
            cod = generarCB60(sitio.id,'998',vencimiento,liq.total,vencimiento2,liq.total,liq.id_liquidacion,liq.fecha.year,liq.fecha.month)
    except:
        cod = generarCB48(sitio.id,'998',vencimiento,liq.total,vencimiento2,liq.total,liq.id_liquidacion,liq.fecha.year,liq.fecha.month)
 
 
       
    path = 'staticfiles/munis/'+settings.MUNI_DIR+'/'
    
    context['codbar'] = armarImgCodBar(cod)
    cod = " ".join(cod[i:i+5] for i in range(0, len(cod), 5)).replace(' ', ' ')
    context['codigo'] = cod
    
    return render_to_pdf_response(request, template, context)

def generarCB48(codMuni,tributo,vencimiento,importe,vencimiento2,importe2,idCuotaLiq,anio,cuota):
    """Genera el código de Barras de 48 dígitos""" 
    #000 001 150120 869520231645821042000000010000000012020015
    cod = ""
    cod += str(codMuni).strip().rjust(3, "0")#CODIGO DEL MUNICIPIO
    cod += str(tributo).strip().rjust(3, "0") #TRIBUTO/LIQUIDACION WEB    
    cod += str(vencimiento.strftime("%d%m%y")).rjust(6, "0") #Vencimiento
    cod += str(importe).strip().replace(".","").rjust(7, "0") #Importe Actualizado
    cod += str(vencimiento2.strftime("%d%m%y")).rjust(6, "0") #Vencimiento2
    cod += str(importe2).strip().replace(".","").rjust(7, "0") #Importe2 Actualizado
    cod += str(idCuotaLiq).strip().rjust(9, "0") #Id Liquidacion
    cod += str(anio).strip().rjust(4, "0") #Anio
    cod += str(cuota).strip().rjust(2, "0") #Cuota    
    cod += str(digVerificador(cod.strip()))    
    return cod

def generarCB60(codMuni,tributo,vencimiento,importe,vencimiento2,importe2,idCuotaLiq,anio,cuota):  
    """Genera el código de Barras de 60 dígitos""" 
    cod = "99999"
    cod += str(codMuni).strip().rjust(3, "0")#CODIGO DEL MUNICIPIO
    cod += str(tributo).strip().rjust(3, "0") #TRIBUTO/LIQUIDACION WEB
    cod += str(vencimiento.strftime("%d%m%y")).rjust(6, "0") #Vencimiento
    cod += str(importe).strip().replace(".","").rjust(10, "0") #Importe Actualizado
    cod += str(vencimiento2.strftime("%d%m%y")).rjust(6, "0") #Vencimiento2
    cod += str(importe2).strip().replace(".","").rjust(10, "0") #Importe2 Actualizado
    cod += str(idCuotaLiq).strip().rjust(10, "0") #Id Cuota
    cod += str(anio).strip().rjust(4, "0") #Anio   
    cod += str(cuota).strip().rjust(2, "0") #Cuota        
    cod += str(digVerificador(cod.strip()))    
    return cod

##########################################################################

@login_required
def calcularPunitoriosForm(request,idc,valor):    
    """Calcula y devuelve intereses de la cuota que se está liquidando en pantalla(AJAX)""" 
    try:
        c = Cuotas.objects.get(id_cuota=idc)
        hoy = date.today()                
        valor = Decimal(valor)        
        importe = punitorios(c,hoy,valor)                                               
    except:
        return HttpResponse('Error!') # Error Manejado

    if request.is_ajax() or settings.DEBUG:                  
        return HttpResponse(str(importe))
    else:
        return HttpResponse('Error!') # Error Manejado
        
@login_required 
def verDDJJDrei(request):              
    """Ver las DDJJ de DReI realizadas por mes/año de algún padrón determinado (para los MUNICIPIOS)""" 
    try:
        sitio = Configuracion.objects.all().first()
    except Configuracion.DoesNotExist:
        sitio = None
        return HttpResponseRedirect(LOGIN_URL)

    form = BusquedaDDJJForm(request.POST or None)  
    fecha = date.today()         
    if form.is_valid():        
        anio = form.cleaned_data['anio']
        mes = form.cleaned_data['mes'] 
        if int(mes)>0:
            boletas = DriBoleta.objects.filter(anio=anio,mes=mes).distinct().order_by('id_cuota__padron','anio','mes')
        else:
            boletas = DriBoleta.objects.filter(anio=anio).distinct().order_by('id_cuota__padron','anio','mes')
        try:
            contribuyente = form.cleaned_data['contribuyente']                         
            if contribuyente:
                boletas = boletas.filter(id_cuota___nombre__icontains=contribuyente)
        except:
            contribuyente = None

        try:
            padron = form.cleaned_data['padron']                         
            if padron:
                boletas = boletas.filter(id_cuota__padron__icontains=padron)
        except:
            padron = None
   
        boleta_detalles = DriBoleta_actividades.objects.filter(id_boleta__in=boletas.values('id_boleta'))\
        .values('id_boleta','id_boleta__anio','id_boleta__mes','id_boleta__vencimiento','id_boleta__total','id_boleta__fechapago','id_boleta__recargo','id_boleta__derecho_neto',\
            'id_boleta__derecho_neto','id_boleta__tasa_salud_publ','id_boleta__adic_detalle','id_boleta__adic_monto','id_boleta__retenciones','id_boleta__minimo_global',\
            'id_boleta__id_cuota__nombre','id_boleta__id_cuota__padron','id_actividad','activ_descr','base','alicuota','minimo','impuesto').order_by('id')
        
    if (request.POST.get('submit') == 'Imprimir') and boleta_detalles:
        context = Context() 
        fecha = datetime.today()                  
        return render_to_pdf_response(request,'drei/reporte_ddjj.html',locals())  
    else:
        return render(request,'municipio.html',locals())

@login_required 
def EliminarBoleta(request,idb):
    """Elimina Boletas liquidadas""" 
    cuota = None
    try:        
        boleta = DriBoleta.objects.get(id_boleta=idb)          
        cuota = boleta.id_cuota
        puedeVerPadron(request,boleta.id_padron)
        if boleta:
            boleta.delete()
        messages.add_message(request, messages.SUCCESS,u'¡La Boleta/Rectif. fué eliminada exitosamente!.')
        return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':cuota.id_padron}))
    except Exception as e:        
        messages.add_message(request, messages.ERROR,u'¡La Boleta/Rectif. no pudo ser eliminada!.')
        if cuota:
            return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':cuota.id_padron}))
        else:
            return volverHome(request)

######################################################################################################################################################

##########################################################################
#      Suscriptores Boleta Digital  - Hace que no les llegue la boleta   #
##########################################################################

def get_suscriptor(idp=None):        
    """Me trae los datos del Suscriptor según el id_padron"""     
    if idp:
        return Suscriptores.objects.filter(id_padron=idp).first()                        
    return None    

def suscripcion_alta(request,idp):
    """ Doy de alta la suscripción WEB, si ya existe actualizo su fecha alta al dia de hoy """
    puedeVerPadron(request,idp)
    c = Cuotas.objects.filter(id_padron=idp).first()        
    if c:
        try:
            obj = Suscriptores.objects.get(id_padron=idp)
            obj.fecha_alta = date.today()
            obj.fecha_baja = None
            obj.save()
        except Suscriptores.DoesNotExist:
            suscr = Suscriptores(tributo=c.tributo,id_padron=idp)
            suscr.save()
        messages.add_message(request, messages.SUCCESS,u'¡La Suscripción fué guardada con éxito!.')            
    else:
        messages.add_message(request, messages.ERROR,u'¡La Suscripción no pudo ser guardada!.')        
    return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':idp}))    

def suscripcion_baja(request,idp):
    """ Doy de baja la suscripción WEB (se marca la fecha de baja) """
    puedeVerPadron(request,idp)
    c = Cuotas.objects.filter(id_padron=idp).first()        
    if c:
        try:
            obj = Suscriptores.objects.get(id_padron=idp)                
            obj.fecha_baja = date.today()
            obj.save()
        except Suscriptores.DoesNotExist:
            messages.add_message(request, messages.ERROR,u'¡La Suscripción no pudo ser guardada!.')                        
            return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':idp}))

        messages.add_message(request, messages.SUCCESS,u'¡La Suscripción fué guardada con éxito!.')            
    else:
        messages.add_message(request, messages.ERROR,u'¡La Suscripción no pudo ser guardada!.')        
    return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':idp}))   

######################################################################################################################################################

##################################################
#      Mandar datos para pago online             #
##################################################

# import requests
# r = requests.post('http://yourdomain/path/', data = {'key':'value'})
from urllib import urlencode
@login_required
def generarPago(request):   
    """ Genero los datos del Pago ONLine (paquete de cuotas seleccionadas para pago) """
    if request.is_ajax():         
        datos = request.GET.getlist('cuotas[]')                                        
        try:
            params = {'cuotas[]': datos}        
            NoComercio = int(getConfigVars().get('NoComercio', {}).get('numero','0'))                       
            url= request.build_absolute_uri('/pago/exito/')+'?'+urlencode(params, True)                                                            
            if datos==[]:               
               raise Exception
        except Exception as e:
            print e.message
            return HttpResponse(json.dumps([]), content_type = "application/json")
        lista = []
        lista.append(url);
        d = []
        if datos:
            i=0            
            for i,idc in enumerate(datos):                
                c = Cuotas.objects.get(id_cuota=idc) 
                if c.tributo.id_tributo==6:
                    boleta = DriBoleta.objects.filter(id_padron=c.id_padron,anio=c.anio,mes=c.cuota).first()
                    total  = calcularPunitorios(request,c,boleta,boleta.total)                        
                else:
                    total  = calcularPunitorios(request,c,None,0)
                                
                importe = total['punit1']
                
                codbar = generarCodBar(idc,importe,importe,None,None)            

                d.append([('Conceptos['+str(i)+'].Concepto', c.get_datos())])
                d.append([('Conceptos['+str(i)+'].Valor', str(importe))])
                d.append([('Conceptos['+str(i)+'].InformacionAdicional', codbar)])                                                

        lista.append(d);
        lista.append(NoComercio);
        return HttpResponse(json.dumps(lista), content_type = "application/json")
    else:
        return HttpResponse("ERROR sólo AJAX")

@login_required
def generarPagoExito(request):
    """ Informa si se pudo registrar con éxito la entrada en CAJERO24, 
    setea el estado de la cuota  en 1000 (estado provisorio para que no se modifique) hasta que se registre el pago en el cajero (vuelve a su estado normal)  """
    idp = None
    try:     
        datos = request.GET.getlist('cuotas[]')
        c = [int(i) for i in datos]        
        cuotas = Cuotas.objects.filter(id_cuota__in=c)        
        cuotas.update(estado=1000)
        idp = cuotas.first().id_padron        
        messages.add_message(request, messages.SUCCESS,u'Los pagos fueron registrados con éxito! (recuerde que el proceso de acreditación puede demorar hasta 48hs hábiles).')        
        return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':idp}))        
    except:
        messages.add_message(request, messages.ERROR,u'Los pagos no pudieron realizarse!.')
        if idp:
            return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':idp}))
        else:
            return volverHome(request)
         

@login_required
def generarPagoError(request,idp):
    """ Informa si no se pudo registrar con éxito la entrada en CAJERO24, de acuerdo a la url devuelta """
    messages.add_message(request, messages.ERROR,u'¡Los pagos no pudieron realizarse!')
    if idp:
        return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':idp}))
    else:
        return volverHome(request)
         




