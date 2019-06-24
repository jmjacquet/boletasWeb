# -*- coding: utf-8 -*-

from django.template import RequestContext,Context
from django.shortcuts import *
from .models import *
from django.views.generic import TemplateView,ListView,CreateView,UpdateView
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
try:
    import json
except ImportError:
    from django.utils import simplejson as json
from datetime import datetime,date
from dateutil.relativedelta import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

####################################################
# Funciones que utilizan varios procedimientos
####################################################

def listado_responsables(request):
    try:
        resps = Responsables.objects.all()
    except Responsables.DoesNotExist:
        raise Http404
    return render_to_response('padrones_representantes.html',{'resps':resps},context_instance=RequestContext(request))

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def padrones_x_estudio(id_estudioc):
    cursor = connection.cursor()
    cursor.execute("SELECT c.id_padron,c.padron,r.nombre as nombreResp,t.abreviatura as tipoTributo\
        FROM dri_estudio_padron dep \
        JOIN cuotas c on (c.id_padron=dep.id_padron) \
        JOIN tributo t on (c.tributo=t.id_tributo) \
        JOIN responsables r on (r.id_responsable=c.id_responsable) \
        WHERE (dep.id_estudioc =  %s)and(t.id_tributo=6) GROUP BY c.id_padron,c.padron order by r.nombre,c.padron",[id_estudioc])
    padrones = dictfetchall(cursor)
    return padrones

def padrones_x_responsable(idResp,idPadron=None):
    padrones = Cuotas.objects.filter(id_responsable=idResp).order_by('tributo','padron','id_padron').values('id_padron','padron','tributo','tributo__descripcion','tributo__abreviatura').annotate(Count('id_padron'))  
    if idPadron:
        padrones=padrones.filter(id_padron=idPadron)
    return padrones

def cuotas_x_padron(idResp,idPadron):
    if idResp is None:
        cuotas = Cuotas.objects.filter(id_padron=idPadron)
    else:
        cuotas = Cuotas.objects.filter(id_padron=idPadron,id_responsable=idResp)
    return cuotas

def responsable_del_padron(idPadr):
    try:
        resp = Cuotas.objects.filter(id_padron=idPadr).order_by('-id_cuota').first().id_responsable
    except Cuotas.DoesNotExist:
        resp = None
    return resp

def puedeVerPadron(request,idPadron,idEstudio):
    try:
        usr=request.user
        tipoUsr=request.user.userprofile.tipoUsr

        if tipoUsr==0:
            idResp = Cuotas.objects.filter(id_padron=idPadron).select_related('id_responsable').order_by('-id_cuota').first().id_responsable.id_responsable        
            if not (int(idResp)==int(usr.userprofile.id_responsable)):
                raise http.Http404
        else:
         if tipoUsr==1:
            try:
                estudio = DriEstudioPadron.objects.filter(id_padron=int(idPadron)).select_related('id_responsable').values_list('id_estudioc',flat=True)
            except ObjectDoesNotExist:
                estudio = None   
                raise http.Http404        
            
            if not (int(idEstudio) in estudio):
                raise http.Http404
    except:
        raise http.Http404

class TienePermisoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().id_estudioc != self.request.user.userprofile.id_estudioc):
            raise http.Http404
        return super(TienePermisoMixin, self).dispatch(request, *args, **kwargs)

##############################################
#      Mixin para cargar las Vars de sistema #
##############################################

class VariablesMixin(object):
    def get_context_data(self, **kwargs):
        context = super(VariablesMixin, self).get_context_data(**kwargs)
        context['idMuni'] = settings.MUNI_ID
        context['dirMuni'] = settings.MUNI_DIR        
        puede_rectificar = 'N'
        try:
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)
            if sitio:
                puede_rectificar = sitio.puede_rectificar
        except Configuracion.DoesNotExist:
            sitio = None            
        context['sitio'] = sitio        
        context['puede_rectificar'] = puede_rectificar        
        context['fecha_hoy'] = date.today()        
        return context

##############################################
#      Padrones de Estudios Contables        #
##############################################


class EstudiosView(VariablesMixin,TemplateView):
    template_name = 'padrones_estudio.html'
    context_object_name = 'estudios'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):        
        return super(EstudiosView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EstudiosView, self).get_context_data(**kwargs)
        idEst= int(self.request.user.userprofile.id_estudioc)
        try:
            estudio=DriEstudio.objects.get(id_estudioc=idEst)
        except DriEstudio.DoesNotExist:
            estudio = None

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

class ResponsablesView(VariablesMixin,TemplateView):
    template_name = 'padrones_representante.html'
    context_object_name = 'padrones'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResponsablesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResponsablesView, self).get_context_data(**kwargs)
        idResp= int(self.request.user.userprofile.id_responsable)
        
        try:
            context['responsable'] = Responsables.objects.get(id_responsable=idResp)
            p = padrones_x_responsable(idResp,None)
            try:
                  sitio = Configuracion.objects.get(id=settings.MUNI_ID)
            except Configuracion.DoesNotExist:
                  sitio = None
            if sitio <> None:
                if (sitio.ver_unico_padron == 'S'):
                 if "usuario" in self.request.session:
                    p = p.filter(padron=self.request.session["usuario"])
                    
            context['padr'] = p 
            context['padron'] = p[0]
        except:
            context['responsable'] = None
            context['padr'] = None
            context['padron'] = None
        return context

##################################################
#      Ver cuotas del Padrón seleccionado        #
##################################################

class BusquedaCuotasView(VariablesMixin,TemplateView):
    template_name = 'cuotas.html'
    context_object_name = 'cuotas'
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        idPadron = self.kwargs.get("idp",'0')
        if self.request.user.userprofile.id_estudioc==None:
            idEst=0
        else:
            idEst= int(self.request.user.userprofile.id_estudioc)        
        puedeVerPadron(self.request,idPadron,idEst)
        
        return super(BusquedaCuotasView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(BusquedaCuotasView, self).get_context_data(**kwargs)
        # En el contrxto pongo el padrón seleccionado asi saco sus características
        idPadron = self.kwargs.get("idp",'0')
        resp = cuotas_x_padron(None,idPadron).select_related('id_responsable').order_by('-id_cuota').first().id_responsable
        idResp = resp.id_responsable
        anio = int(self.kwargs.get("anio",'0'))
        context['anio']=anio
        context['responsable'] = resp
        context['padr'] = padrones_x_responsable(idResp,None)        
        if idResp:
            if idPadron:
                try:
                    p = padrones_x_responsable(idResp,idPadron).first()
                except IndexError:
                    p = None
                context['padron']=p

        c = Cuotas.objects.raw("SELECT c.*,db.id_boleta as boleta,db.pago_anterior as pago_anterior,db.minimo_global as minimo_global,db.total as total,db.fechapago as boleta_venc FROM cuotas c LEFT JOIN dri_boleta db on (c.id_cuota=db.id_cuota) WHERE c.id_padron = %s order by c.vencimiento DESC",[idPadron])
        # c = c.order_by('-vencimiento')
        if (anio>0):
            c = Cuotas.objects.raw("SELECT c.*,db.id_boleta as boleta,db.pago_anterior as pago_anterior,db.minimo_global as minimo_global,db.total as total,db.fechapago as boleta_venc FROM cuotas c LEFT JOIN dri_boleta db on (c.id_cuota=db.id_cuota) WHERE (c.id_padron = %s)and(c.anio = %s) order by c.vencimiento DESC",[idPadron,anio])
        context['cuotas'] = c
        context['cant_cuotas'] = len(list(c))
        return context

##########################################################################3
def armarCodBar(cod):
    import imprimirPDF
    b  = imprimirPDF.get_image2(cod)
    return b

from easy_pdf.rendering import render_to_pdf_response
def imprimirPDF(request,idc,idb=None):       
    from Code128 import Code128
    from base64 import b64encode
        
    try:
        c = Cuotas.objects.get(id_cuota=idc) 
    except:
        raise Http404

    try:
       if request.user.userprofile.id_estudioc==None:
            idEst=0
       else:
            idEst= int(request.user.userprofile.id_estudioc)
    except:
        idEst=0
    
    puedeVerPadron(request,c.id_padron,idEst)       

    diasExtra = None
    try:
        sitio = Configuracion.objects.get(id=settings.MUNI_ID)
        diasExtra = sitio.diasextravencim
    except Configuracion.DoesNotExist:
        sitio = None
    
    if not sitio:    
        raise http.Http404

    if diasExtra == None:
        diasExtra=0

    hoy = date.today()

    if (hoy >= c.vencimiento):
        vencimiento = hoy + relativedelta(days=diasExtra)   
        vencimiento2 = vencimiento
    else:
        vencimiento = c.vencimiento
        if c.segundo_vencimiento==None:
           vencimiento2 = vencimiento + relativedelta(months=1)
        else:
            vencimiento2 = c.segundo_vencimiento   

    context = Context()    
    context['cuota'] = c
    context['idMuni'] = settings.MUNI_ID
    context['dirMuni'] = settings.MUNI_DIR
    context['fecha'] = datetime.now()
    context['vencimiento'] = vencimiento
    context['codseg'] = c.id_responsable.codseg
    context['sitio'] = sitio
    
       
 
    if c.tributo.id_tributo == 6 :
       template ='boletas/boleta_drei.html'
       try:
        if idb:
            boleta = DriBoleta.objects.filter(id_boleta=idb).first()
            context['titulo']=u'Boleta Rectificativa DReI'
        else:
            boleta = DriBoleta.objects.filter(id_cuota=c).first()
            context['titulo']=u'Boleta Liquidación DReI'
       
        a = DriBoleta_actividades.objects.filter(id_boleta=boleta).select_related('id_actividad')       
       except:
         raise Http404

       try:
            minimo_principal = DriPadronActividades.objects.filter(id_padron=boleta.id_padron,principal='S').values('monto_minimo').first()
       except:
            minimo_principal = 0

       tot_adicionales =  boleta.recargo + boleta.derecho_neto + boleta.tasa_salud_publ + boleta.adic_monto + boleta.retenciones
       total_importe = tot_adicionales + boleta.total       
       totales = calcularPunitorios(request,c,boleta,boleta.total)     
       totOrig = a.aggregate(Sum('impuesto'))
       context['actividades'] = a
       
       try:
            if boleta.minimo_global <= 0:
                # si es boleta vieja vencida le pongo el saldo de la cuota (minimo de ese momento)
                if (hoy > c.vencimiento):
                    context['minimo_principal'] = c.saldo
                else:
                    context['minimo_principal'] = minimo_principal['monto_minimo'] 
            else:
                context['minimo_principal'] = boleta.minimo_global            
       except:
            context['minimo_principal'] = minimo_principal['monto_minimo'] 
       
       if totOrig['impuesto__sum'] <= context['minimo_principal']:
            context['totOriginal'] = context['minimo_principal'] 
       else: 
            context['totOriginal'] = totOrig['impuesto__sum'] 

       context['boleta'] = boleta
       context['subtotal'] = format(boleta.total, '.2f')       
       context['tot_adicionales'] = tot_adicionales
       context['vencimiento2'] = vencimiento
       vencimiento2 = vencimiento
       total1 = boleta.total
       total2 = boleta.total
       total1 = format(total1, '.2f')
       total2 = format(total2, '.2f')
       
       #totales = calcularPunitorios(request,c,boleta,totOrig['impuesto__sum'])
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
    
    if ((hoy >= c.vencimiento)and(c.tributo.id_tributo != 6)):
        vencimiento = c.vencimiento
        total1 = c.saldo

    try:        
        if sitio.longitudCodigoBarra==60:
            cod = generarCB60(sitio.id,c.tributo.id_tributo,vencimiento,total1,vencimiento2,total2,c.id_cuota,c.anio,c.cuota)

        else:
            cod = generarCB48(sitio.id,c.tributo.id_tributo,vencimiento,total1,vencimiento2,total2,c.id_cuota,c.anio,c.cuota)
    except:
            cod = generarCB48(sitio.id,c.tributo.id_tributo,vencimiento,total1,vencimiento2,total2,c.id_cuota,c.anio,c.cuota)
    
    path = 'staticfiles/munis/'+settings.MUNI_DIR+'/'
    
    context['codbar'] = armarCodBar(cod)
    context['codigo'] = cod
    
    return render_to_pdf_response(request, template, context)

##################################################
#     Liquidacion DReI                         #
##################################################
from django.forms.models import inlineformset_factory
from .forms import LiqDreiBoletaForm,LiqDreiActivForm,EstudioForm,ResponsableForm,AgregarDDJJForm,BusquedaDDJJForm,LiqDreiRectifForm
from django.db import transaction
from django.contrib.messages import constants as message_constants

class DreiLiquidarCreateView(VariablesMixin,CreateView):
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
        cuota = Cuotas.objects.get(id_cuota=idc)                 
        try:
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if cuota:            
            context['cuota'] = cuota        
            context['responsable'] = Responsables.objects.get(id_responsable=cuota.id_responsable.id_responsable)                       
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        
        context['titulo'] = u'Autoliquidación de Boletas de DReI'       
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        context = self.get_context_data()
        cuota = context['cuota']    
        try:
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        minGlobal=0
        minimo = 0
        hoy = date.today()        
        actividades = DriPadronActividades.objects.filter(id_padron=cuota.id_padron).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).filter(fecha_inicio__lte=hoy).select_related('id_actividad')        
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)
        data_activ = []
        if actividades.count()>0:
            for activ in actividades:
                if activ.monto_minimo is None:
                    minimo = 0
                if activ.principal != 'S':
                    minimo = 0
                else:
                    if sitio.minimo_por_activ=='S':
                       minimo = activ.monto_minimo
                
                    minGlobal=minimo

                if activ.id_actividad.alicuota is None:
                    alicuota = 0
                else:
                    alicuota = activ.id_actividad.alicuota
           
                data_activ.append({'id_actividad': activ.id_actividad.id_actividad,'minimo':minimo,'alicuota':alicuota,
                    'activ_descr':activ.verDetalleActiv(),'base':'0','impuesto':'0'})
                        
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
        cuota = context['cuota']
        hoy = date.today()       
        self.object.id_cuota = cuota
        self.object.save()
        for forma in actividades_formset:
            forma.id_boleta = self.object.id_boleta  
            hoy = date.today()                                                
            try:                
                dria=DriPadronActividades.objects.filter(id_padron=self.object.id_padron,id_actividad=forma.id_actividad).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).first()             
                forma.activ_descr = dria.verDetalleActiv()                        
            except:
                dria=None
                forma.activ_descr = ''            
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
        actividades = DriPadronActividades.objects.filter(id_padron=cuota.id_padron).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).filter(fecha_inicio__lte=hoy).select_related('id_actividad')
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)        
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades')
        minimo = form.cleaned_data['minimo_global']    
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))


class DreiLiquidarUpdateView(VariablesMixin,UpdateView):
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
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if boleta:
            cuota = boleta.id_cuota            
            context['cuota'] = cuota        
            context['responsable'] = Responsables.objects.get(id_responsable=cuota.id_responsable.id_responsable)
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        context['titulo'] = u'Reliquidar Boleta de DReI'       
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        try:
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        boleta = self.object        
        if boleta:
            cuota = boleta.id_cuota
            hoy = date.today()             
            dri_activ = DriPadronActividades.objects.filter(id_padron=cuota.id_padron).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).filter(fecha_inicio__lte=hoy)
            dria = dri_activ.values_list('id_actividad',flat=True)        
            boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta)
            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',max_num=dria.count(),can_delete=False,form=LiqDreiActivForm)                    
            data_activ = []
            for activ in boleta_activ:                
                if activ.id_actividad.id_actividad in dria:
                    data_activ.append({'id_actividad':activ.id_actividad.id_actividad,'activ_descr':activ.verDetalleActiv(),'base':activ.base,'alicuota':activ.alicuota,'minimo':activ.minimo,'impuesto':activ.impuesto})                            

            if len(data_activ)==0:
                minimo = 0
                alicuota = 0

                #cargo las actividades como que fuese una boleta nueva
                if dri_activ.count()>0:
                    for activ in dri_activ:
                        if activ.monto_minimo is None:
                            minimo = 0
                        if activ.principal != 'S':
                            minimo = 0
                        else:
                            if sitio.minimo_por_activ=='S':
                               minimo = activ.monto_minimo

                        if activ.id_actividad.alicuota is None:
                            alicuota = 0
                        else:
                            alicuota = activ.id_actividad.alicuota
                   
                        data_activ.append({'id_actividad': activ.id_actividad.id_actividad,'minimo':minimo,'alicuota':alicuota,
                            'activ_descr':activ.verDetalleActiv(),'base':'0','impuesto':'0'})
            
            minGlobal=boleta.minimo_global
            if sitio:
                if (sitio.minimo_por_activ=='N'):
                    minGlobal=cuota.saldo
                        
            data = {'minimo_global':minGlobal}

            form = LiqDreiBoletaForm(instance=boleta,initial=data)
            if boleta.adic_detalle:
                adic = [item for item in ADICIONALES if item[1] == boleta.adic_detalle]           
                form.fields['adic_select'].initial = int(adic[0][0])
            
            
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
        for forma in actividades_formset:
            forma.id_boleta = self.object.id_boleta  
            hoy = date.today()                                                
            try:                
                dria=DriPadronActividades.objects.filter(id_padron=self.object.id_padron,id_actividad=forma.id_actividad).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).first()               
                forma.activ_descr = dria.verDetalleActiv()                     
            except:
                dria=None
                forma.activ_descr = ''            
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
        if boleta:
            hoy = date.today()
            cuota = boleta.id_cuota
            boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta)
            dria = DriPadronActividades.objects.filter(id_padron=cuota.id_padron).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).filter(fecha_inicio__lte=hoy).values_list('id_actividad',flat=True)        
            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',max_num=dria.count(),can_delete=False,form=LiqDreiActivForm)                    
            data_activ = []
            for activ in boleta_activ:                
                if activ:
                    data_activ.append({'id_actividad':activ.id_actividad.id_actividad,'activ_descr':activ.verDetalleActiv()})                
            actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades',initial=data_activ)
        else:
            return HttpResponseRedirect('/')    
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))


#################################################################
class DreiRectificarNew(VariablesMixin,CreateView):
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
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if cuota:            
            context['cuota'] = cuota        
            context['responsable'] = Responsables.objects.get(id_responsable=cuota.id_responsable.id_responsable)           
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        context['titulo'] = u'Rectificativa de Boletas de DReI'       
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        context = self.get_context_data()
        cuota = context['cuota']    
        try:
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        minGlobal=0
        minimo = 0
        hoy = date.today()        
        actividades = DriPadronActividades.objects.filter(id_padron=cuota.id_padron).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).filter(fecha_inicio__lte=hoy).select_related('id_actividad')        
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)
        data_activ = []
        if actividades.count()>0:
            for activ in actividades:
                if activ.monto_minimo is None:
                    minimo = 0
                if activ.principal != 'S':
                    minimo = 0
                else:
                    if sitio.minimo_por_activ=='S':
                       minimo = activ.monto_minimo
                
                    minGlobal=minimo

                if activ.id_actividad.alicuota is None:
                    alicuota = 0
                else:
                    alicuota = activ.id_actividad.alicuota
           
                data_activ.append({'id_actividad': activ.id_actividad.id_actividad,'minimo':minimo,'alicuota':alicuota,
                    'activ_descr':activ.verDetalleActiv(),'base':'0','impuesto':'0'})
                        
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
        cuota = context['cuota']
        hoy = date.today()       
        self.object.id_cuota = cuota
        self.object.save()
        for forma in actividades_formset:
            forma.id_boleta = self.object.id_boleta  
            hoy = date.today()                                                
            try:                
                dria=DriPadronActividades.objects.filter(id_padron=self.object.id_padron,id_actividad=forma.id_actividad).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).first()              
                forma.activ_descr = dria.verDetalleActiv()                        
            except:
                dria=None
                forma.activ_descr = ''            
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
        cuota = context['cuota']
        hoy = date.today()       
        actividades = DriPadronActividades.objects.filter(id_padron=cuota.id_padron).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).filter(fecha_inicio__lte=hoy).select_related('id_actividad')
        ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',extra=actividades.count(),can_delete=False,form=LiqDreiActivForm)        
        actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades')
            
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

class DreiRectificar(VariablesMixin,CreateView):
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
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')    
        if boleta:
            cuota = boleta.id_cuota            
            context['cuota'] = cuota        
            context['responsable'] = Responsables.objects.get(id_responsable=cuota.id_responsable.id_responsable)
            context['minimo_por_activ'] = sitio.minimo_por_activ        
        context['titulo'] = u'Rectificativa de Boletas de DReI'       
        return context

    def get(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form_class = self.get_form_class()        
        form = self.get_form(form_class)
        boleta =  self.object      
        try:
            sitio = Configuracion.objects.get(id=settings.MUNI_ID)            
        except Configuracion.DoesNotExist:
            sitio = None
            return HttpResponseRedirect('/')  
        if boleta:
            cuota = boleta.id_cuota
            hoy = date.today() 
            dri_activ = DriPadronActividades.objects.filter(id_padron=cuota.id_padron).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).filter(fecha_inicio__lte=hoy)
            dria= dri_activ.values_list('id_actividad',flat=True)        
            
            boleta_activ = DriBoleta_actividades.objects.filter(id_boleta=boleta)            
            ActividadesFormSet = inlineformset_factory(DriBoleta,DriBoleta_actividades,fk_name='id_boleta',max_num=dria.count(),can_delete=False,form=LiqDreiActivForm)                    
            data_activ = []
            for activ in boleta_activ:                                
                if activ.id_actividad.id_actividad in dria:
                    data_activ.append({'id_actividad':activ.id_actividad.id_actividad,'activ_descr':activ.verDetalleActiv(),'base':activ.base,'alicuota':activ.alicuota,'minimo':activ.minimo,'impuesto':activ.impuesto})                

            if len(data_activ)==0:
                minimo = 0
                alicuota = 0
                #cargo las actividades como que fuese una boleta nueva
                if dri_activ.count()>0:
                    for activ in dri_activ:
                        if activ.monto_minimo is None:
                            minimo = 0
                        if activ.principal != 'S':
                            minimo = 0
                        else:
                            if sitio.minimo_por_activ=='S':
                               minimo = activ.monto_minimo

                        if activ.id_actividad.alicuota is None:
                            alicuota = 0
                        else:
                            alicuota = activ.id_actividad.alicuota
                   
                        data_activ.append({'id_actividad': activ.id_actividad.id_actividad,'minimo':minimo,'alicuota':alicuota,
                            'activ_descr':activ.verDetalleActiv(),'base':'0','impuesto':'0'})

            
            data = {'id_padron': boleta.id_padron,'anio': boleta.anio,'mes': boleta.mes,'vencimiento': boleta.vencimiento,'total':boleta.total,
                        'recargo':boleta.recargo,'derecho_neto':boleta.derecho_neto,'tasa_salud_publ':boleta.tasa_salud_publ,'retenciones':boleta.retenciones,
                        'adic_monto':boleta.adic_monto,'id_cuota':boleta.id_cuota,'minimo_global':boleta.minimo_global}

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
        for forma in actividades_formset:
            forma.id_boleta = self.object.id_boleta  
            hoy = date.today()                                                
            try:                
                dria=DriPadronActividades.objects.filter(id_padron=self.object.id_padron,id_actividad=forma.id_actividad).filter(Q(fecha_fin__gte=hoy)|Q(fecha_fin=None)).first()              
                forma.activ_descr = dria.verDetalleActiv()                     
            except:
                dria=None
                forma.activ_descr = ''            
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
                    data_activ.append({'id_actividad':activ.id_actividad.id_actividad,'activ_descr':activ.verDetalleActiv()})                
            actividades_formset = ActividadesFormSet(self.request.POST,prefix='actividades',initial=data_activ)
            
        return self.render_to_response(self.get_context_data(form=form,actividades_formset=actividades_formset))

####################################################################################        
@login_required
def verificarCuota(request,idc):
    if request.is_ajax():
        cuota = Cuotas.objects.get(id_cuota=idc)  
        boleta = DriBoleta.objects.filter(id_padron=cuota.id_padron,anio=cuota.anio,mes=cuota.cuota)
        if boleta:
            data = {'msj': "La boleta %s/%s ya se encuentra liquidada!!" % (cuota.cuota,cuota.anio),'url':""}
        else:
            data = {'msj': "",'url': reverse('drei_liquidarBoleta', kwargs={'idc':idc})}
        return HttpResponse(json.dumps(data), content_type='application/json')

##################################################
#      Ver DDJJ Presentadas                      #
##################################################

class DreiDDJJAList(VariablesMixin,ListView):
    template_name = 'drei/drei_ddjj_listado.html'
    context_object_name = 'ddjj'
    
    def dispatch(self, *args, **kwargs):
        anio = int(self.kwargs.get("anio",'0'))
        idPadron = self.kwargs.get("idp",'0')
        if self.request.user.userprofile.id_estudioc==None:
            idEst=0
        else:
            idEst= int(self.request.user.userprofile.id_estudioc)
        puedeVerPadron(self.request,idPadron,idEst)
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
        resp = cuotas_x_padron(None,idPadron).select_related('id_responsable').order_by('-id_cuota')[0].id_responsable
        idResp = resp.id_responsable
        anio = int(self.kwargs.get("anio",'0'))
        context['anio']=anio
        context['responsable'] = resp
        context['padr'] = padrones_x_responsable(idResp,None)        
        if idResp:
            if idPadron:
                try:
                    p = padrones_x_responsable(idResp,idPadron)[0]
                except IndexError:
                    p = None
                context['padron']=p
        return context

##################################################
#      Update de Estudios                        #
##################################################
class EstudiosUpdateView(VariablesMixin,TienePermisoMixin,UpdateView):
    template_name = 'estudio_update.html'
    model = DriEstudio
    success_url = '/'
    form_class = EstudioForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):        
        return super(EstudiosUpdateView, self).dispatch(*args, **kwargs)

####################################################

def mandarEmailEstudio(request,usrEstudio):
    from smtplib import SMTP
    from email.mime.text import MIMEText as text
    if request.is_ajax:
        message=''                
        try:
            estudio = DriEstudio.objects.filter(usuario=usrEstudio).first()
        except IndexError:
            estudio = None            
            message = "El usuario es incorrecto."
            return HttpResponse(message)
        
        login_valid = (estudio <> None)
        
        if login_valid:
            to_addr=estudio.email
            if to_addr=='':
                return HttpResponse('El estudio no tiene asignada una dirección de e-mail. Por favor verifique.')
            clave = estudio.clave
            from_addr = 'contacto@grupoguadalupe.com.ar'
            msg = u'Ud. ha solicitado el envio de su password por email.\nSu password es: %s' % clave

            m = text(msg)

            m['Subject'] = 'Password Requerido Estudio Contable (Sistema Liquidacion OnLine)'
            m['From'] = from_addr
            m['To'] = to_addr    
            s = SMTP()
            s.connect('smtp.webfaction.com')
            s.login('grupogua_errores','qwerty')
            s.sendmail(from_addr, to_addr, m.as_string())
            message=u"Se envió correctamente el e-mail."            
        return HttpResponse(message)

def calcularPunitorios(request,c,boleta=None,importe=0):
    try:
        cuota = c       
        hoy = date.today()  
        vencimiento = cuota.vencimiento

        if cuota.segundo_vencimiento==None:
           vencimiento2 = vencimiento + relativedelta(months=1)
        else:
            vencimiento2 = cuota.segundo_vencimiento           

        fecha = hoy  

        if cuota.tributo.id_tributo==6 :
            hoy = hoy 
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
            
            importe1 =  importe + punitorios(cuota,vencimiento,fecha)
            importe2 =  importe + punitorios(cuota,vencimiento,vencimiento2)
            #if settings.DEBUG:
                # print importe
                # print importe1
                # print importe2
                # print vencimiento
                # print vencimiento2
                # print fecha
            punit1 = importe1 
            
            porc1 = importe1 - importe
            punit2 = punit1
            porc2 =  porc1
        
        else:
            
            if (hoy<=vencimiento):
                fecha=vencimiento                          
            elif ((hoy>vencimiento)and(hoy<=vencimiento2)):
                fecha=vencimiento2
            else:
                fecha=hoy
                vencimiento2=fecha
                
            
            importe1 = cuota.saldo + punitorios(cuota,vencimiento,fecha)            
           
            punit1 = importe1
            porc1 = importe1 - cuota.saldo
            if cuota.tributo.interes_2ven==0:
                importe2 = importe1
                punit2 = punit1
                porc2 = porc1
            else:                
                importe2 = cuota.saldo + punitorios(cuota,vencimiento,vencimiento2)
                punit2 = importe2
                porc2 =  importe2 - cuota.saldo 

    except:
        return HttpResponse('Error') # Error Manejado
    # if settings.DEBUG:
    #     print 'por1:'+str(importe1)+' porc1:'+str(porc1)+' punit1:'+str(punit1)+' por2:'+str(importe2)+' porc2:'+str(porc2)+' punit2:'+str(punit2)
    return {'punit1': format(punit1, '.2f'), 'porc1': format(porc1, '.2f'),'punit2': format(punit2, '.2f'), 'porc2': format(porc2, '.2f')}

##########################################################################
# Funciones ajax para la liquidacion y cálculo de Punitorios ONLINE
@login_required
def calcularPunitoriosForm(request,idc):
    try:
        c = Cuotas.objects.get(id_cuota=idc)
        hoy = date.today() 
        saldo = c.saldo
        punit = punitorios(c,c.vencimiento,hoy)                        
        por1=0
        try:
            if saldo==0:                
                try:
                    b = DriBoleta.objects.get(id_cuota__id_cuota=idc)                                                                            
                    saldo = b.total        
                    por1 = punit/saldo
                except:
                    por1 = get_interes(c,c.vencimiento,hoy)                    
            else:
                por1 = punit/saldo        
        except:
            por1=0
       
    except:
        return HttpResponse('Error!') # Error Manejado

    if request.is_ajax() or settings.DEBUG:          
        
        return HttpResponse(str(por1))
    else:
        return HttpResponse('Error!') # Error Manejado

@login_required
def generarPunitoriosLiq(request,idp):   
    if request.is_ajax():         
            datos = request.GET.getlist('cuotas[]')            
            
            cuotasAct = {}            
            if datos:
                for i in datos:
                    c = Cuotas.objects.get(id_cuota=i) 
                    if c.tributo.id_tributo==6:
                        boleta = DriBoleta.objects.filter(id_padron=c.id_padron,anio=c.anio,mes=c.cuota)[0]
                        total  = calcularPunitorios(request,c,boleta,boleta.total)                        
                    else:
                        total  = calcularPunitorios(request,c,None,0)
                    cuotasAct[i]=total['punit1']                    
                    
                    # subtotal = subtotal + float(totales['punit1'])
            return HttpResponse(json.dumps(cuotasAct), content_type = "application/json")

@login_required
def generarLiquidacion(request,idp):   
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
                diasExtra = Configuracion.objects.get(id=settings.MUNI_ID).diasextravencim
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
                    messages.add_message(request, messages.SUCCESS,u'Se generó la Liquidación Nº %s exitosamente!.'  % (liq.pk))
                
            return HttpResponse(json.dumps(liq.id_liquidacion), content_type = "application/json")

@login_required
def imprimirPDFLiqWeb(request,id_liquidacion):   
    
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
        sitio = Configuracion.objects.get(id=settings.MUNI_ID)
        diasExtra = sitio.diasextravencim

    except Configuracion.DoesNotExist:
        sitio = None
        return HttpResponseRedirect(LOGIN_URL)
        
    if diasExtra == None:
        diasExtra=0

    hoy = date.today()

    vencimiento = liq.vencimiento
    vencimiento2 = vencimiento
 
    context = Context()    
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
        cod = generarCB48(sitio.id,'998',vencimiento,liq.total,vencimiento2,liq.total,liq.id_liquidacion,liq.fecha.year,liq.fecha.month)
    
        if sitio.longitudCodigoBarra==60:
            cod = generarCB60(sitio.id,'998',vencimiento,liq.total,vencimiento2,liq.total,liq.id_liquidacion,liq.fecha.year,liq.fecha.month)
    except:
        cod = generarCB48(sitio.id,'998',vencimiento,liq.total,vencimiento2,liq.total,liq.id_liquidacion,liq.fecha.year,liq.fecha.month)
 
 
       
    path = 'staticfiles/munis/'+settings.MUNI_DIR+'/'
    
    context['codbar'] = armarCodBar(cod)
    context['codigo'] = cod
    
    return render_to_pdf_response(request, template, context)

def generarCB48(codMuni,tributo,vencimiento,importe,vencimiento2,importe2,idCuotaLiq,anio,cuota):
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

def boletas_x_padron(idResp,idPadron):
    if idResp is None:
        boletas = DriBoleta.objects.filter(id_padron=idPadron)
    else:
        boletas = DriBoleta.objects.filter(id_padron=idPadron,id_cuota__id_responsable=idResp)
    return boletas

##########################################################################

def get_interes(cuota,vencimiento,fecha_punit):
    
    porc = 0
    total = 0
    try:      
        fecha_punit = fecha_punit
        if cuota.segundo_vencimiento==None:
           vencimiento2 = vencimiento + relativedelta(months=1)
        else:
           vencimiento2 = cuota.segundo_vencimiento   

        tipo_interes = cuota.tributo.tipo_interes
        interes = cuota.tributo.interes
        dias=0
        meses=0
        interes_especial = False        
        #Si no tiene definido el interés, lo busco en la configuración
        if interes == None:           
           interes = Configuracion.objects.get(id=settings.MUNI_ID).punitorios
           
        if tipo_interes == None:            
           tipo_interes = Configuracion.objects.get(id=settings.MUNI_ID).tipo_punitorios

        if tipo_interes == None:
           tipo_interes = 1 
        
        if interes == None:
           interes = 0 
         
        #DIARIO
        if tipo_interes == 2:
            try:
                dias = (fecha_punit - vencimiento).days
            except:
                dias = 0
            if dias < 0:
                dias = 0 
            porc =  (interes / 30 ) * dias
        #MENSUAL
        elif tipo_interes == 1:
            try:
                meses = (fecha_punit - vencimiento).days / 30
            except:
                meses = 0
            if meses < 0:
                meses = 0 
            porc =  (interes * meses)        
        
        # Tipo 99 con intereses en el seg y terc venc adicionales
        elif tipo_interes == 99:
            # try:
                dias = (fecha_punit-vencimiento).days
                
                
                coeficiente_acum = 0
                interes_2 = cuota.tributo.interes_2
                

                if interes_2 == None:
                    interes_2 = 0
                
                ven2 = cuota.tributo.vence_dias2
                
                if ven2 == None:
                    ven2 = 0

                # if settings.DEBUG:
                #     print fecha_punit
                #     print vencimiento
                #     print vencimiento2
                #     print interes                

                if ((fecha_punit > vencimiento) and (fecha_punit <= vencimiento2)):
                      coeficiente_acum = coeficiente_acum + interes;
                      fecha_punit = vencimiento2
                      vencimiento = vencimiento2

                if ((fecha_punit > vencimiento2) and (fecha_punit <= (vencimiento + relativedelta(days=ven2)))):
                      coeficiente_acum = coeficiente_acum + interes_2
                      fecha_punit = vencimiento + relativedelta(days=ven2)
                      vencimiento = vencimiento + relativedelta(days=ven2)

                if (fecha_punit > (vencimiento + relativedelta(days=ven2))):
                      coeficiente_acum = coeficiente_acum + interes_2
                      vencimiento = vencimiento + relativedelta(days=ven2)

                # if (fecha_punit == vencimiento):
                #   coeficiente_acum = 0;
                #   fecha_punit = vencimiento
                #   vencimiento = vencimiento

                # if settings.DEBUG:
                #     print coeficiente_acum
                #     print fecha_punit
                #     print vencimiento
                #     print "HASTA ACA"

                interes = Configuracion.objects.get(id=settings.MUNI_ID).punitorios
                tipo_interes = Configuracion.objects.get(id=settings.MUNI_ID).tipo_punitorios
                if interes == None:           
                   interes = 0
                   
                if tipo_interes == None:            
                   tipo_interes = 1
                
                interes_especial= True

                if tipo_interes == 2:
                    try:
                        dias = (fecha_punit - vencimiento).days
                    except:
                        dias = 0
                    if dias < 0:
                        dias = 0

                    porc =  (interes / 30 ) * dias

                #MENSUAL
                elif tipo_interes == 1:
                    try:
                        meses = (fecha_punit - vencimiento).days / 30
                    except:
                        meses = 0
                    if meses < 0:
                        meses = 0 
                    porc =  (interes * meses)        

                if (porc < 0):
                    porc = 0
                    coeficiente_acum = 0

                coeficiente_acum = coeficiente_acum + porc
                porc = coeficiente_acum
                
                if (porc < 0):
                    porc=0

                # if settings.DEBUG:
                #     print dias
                #     print porc
                #     print coeficiente_acum
                #     print vencimiento
                #     print vencimiento2
                #     print fecha_punit
      
        else:
            try:
                dias = (fecha_punit - vencimiento).days
            except:
                dias = 0
            if dias < 0:
                dias = 0 
            porc =  (interes / 30 ) * dias
        
        if porc < 0:
            porc = 0

    except:
        return HttpResponse('Error') # incorrect post
    return porc

def punitorios_rango(cuota,vencimiento,fecha_punit):
    from .models import Configuracion
    porc = 0
    total = 0
    importe = 0
    try:      
        fecha_punit = fecha_punit
        if cuota.segundo_vencimiento==None:
           vencimiento2 = vencimiento + relativedelta(months=1)
        else:
           vencimiento2 = cuota.segundo_vencimiento   
        tipo_interes = cuota.tributo.tipo_interes
        interes = cuota.tributo.interes
        dias=0
        meses=0

        #Si no tiene definido el interés, lo busco en la configuración
        if interes == None:           
           interes = Configuracion.objects.get(id=settings.MUNI_ID).punitorios
           
        if tipo_interes == None:            
           tipo_interes = Configuracion.objects.get(id=settings.MUNI_ID).tipo_punitorios

        if tipo_interes == 10:
            from .models import TributoInteres
            
            tributo_interes = TributoInteres.objects.filter(id_tributo=cuota.tributo.id_tributo,hasta__gte=vencimiento).order_by('desde')
            
    
            #Por cada coeficiente que corresponda hago un calculo
            
            for t in tributo_interes:
                    dias=0
                    meses=0
                    
                    try:                
                       interes = t.interes
                       tipo_interes = t.tipo_interes              
                    except TributoInteres.DoesNotExist:                       
                       tipo_interes = None
                       interes = None                             

                    if tipo_interes == None:
                       tipo_interes = 1 
                    
                    if interes == None:
                       interes = 0 
                    # if settings.DEBUG:
                    #     print interes
                    #     print tipo_interes                      

                    #DIARIO
                    if tipo_interes == 2:                        
                        try:
                            if (vencimiento >= t.desde):
                                if (fecha_punit >= t.hasta):
                                    dias = (t.hasta - vencimiento).days
                                else:
                                    dias = (fecha_punit - vencimiento).days
                            elif (fecha_punit >= t.desde):
                                dias = (fecha_punit - t.desde).days
                            else:
                                dias = 0                                                   
                        except:
                            dias = 0
                        if dias < 0:
                            dias = 0 
                        porc =  (interes / 30 ) * dias
                    #MENSUAL
                    elif tipo_interes == 1:
                        try:
                            if (vencimiento >= t.desde):
                                if (fecha_punit >= t.hasta):
                                    meses = (t.hasta - vencimiento).days / 30
                                else:
                                    meses = (fecha_punit - vencimiento).days / 30
                            elif (fecha_punit >= t.desde):
                                meses = (fecha_punit - t.desde).days / 30
                            else:
                                meses = 0                            
                        except:
                            meses = 0
                        if meses < 0:
                            meses = 0 
                        porc =  (interes * meses)                            
                    else:
                        try:
                            if (vencimiento >= t.desde):
                                if (fecha_punit >= t.hasta):
                                    dias = (t.hasta - vencimiento).days
                                else:
                                    dias = (fecha_punit - vencimiento).days
                            elif (fecha_punit >= t.desde):
                                dias = (fecha_punit - t.desde).days
                            else:
                                dias = 0                            
                        except:
                            dias = 0
                        if dias < 0:
                            dias = 0 
                        porc =  (interes / 30 ) * dias

                    if porc < 0:
                        porc = 0
                                        
                    try:
                        saldo=cuota.saldo
                        if saldo==0:
                            b = DriBoleta.objects.get(id_cuota=cuota)                            
                            saldo = b.total                            
                    except:
                        saldo=0

                    total = saldo * (porc)
                    importe += total

                    # if settings.DEBUG:
                    #     print 'Interes:'+str(interes)+' TipoInteres:'+str(tipo_interes)+' Total:'+str(total)+' Dias:'+str(dias)+' Meses:'+str(meses)
                    
    except Exception as e:
        print e
    return importe

def punitorios(cuota,vencimiento,fecha_punit):
    
    porc = 0
    total = 0
    try:      
        fecha_punit = fecha_punit
        if cuota.segundo_vencimiento==None:
           vencimiento2 = vencimiento + relativedelta(months=1)
        else:
           vencimiento2 = cuota.segundo_vencimiento   

        tipo_interes = cuota.tributo.tipo_interes
        interes = cuota.tributo.interes
        dias=0
        meses=0
        interes_especial = False        
        #Si no tiene definido el interés, lo busco en la configuración
        if interes == None:           
           interes = Configuracion.objects.get(id=settings.MUNI_ID).punitorios
           
        if tipo_interes == None:            
           tipo_interes = Configuracion.objects.get(id=settings.MUNI_ID).tipo_punitorios

        if tipo_interes == 10:
           return punitorios_rango(cuota,vencimiento,fecha_punit)

        if tipo_interes == None:
           tipo_interes = 1 
        
        if interes == None:
           interes = 0 
         
        #DIARIO
        if tipo_interes == 2:
            try:
                dias = (fecha_punit - vencimiento).days
            except:
                dias = 0
            if dias < 0:
                dias = 0 
            porc =  (interes / 30 ) * dias
        #MENSUAL
        elif tipo_interes == 1:
            try:
                meses = (fecha_punit - vencimiento).days / 30
            except:
                meses = 0
            if meses < 0:
                meses = 0 
            porc =  (interes * meses)        
        
        # Tipo 99 con intereses en el seg y terc venc adicionales
        elif tipo_interes == 99:
            # try:
                dias = (fecha_punit-vencimiento).days
                
                
                coeficiente_acum = 0
                interes_2 = cuota.tributo.interes_2
                

                if interes_2 == None:
                    interes_2 = 0
                
                ven2 = cuota.tributo.vence_dias2
                
                if ven2 == None:
                    ven2 = 0

                # if settings.DEBUG:
                #     print fecha_punit
                #     print vencimiento
                #     print vencimiento2
                #     print interes                

                if ((fecha_punit > vencimiento) and (fecha_punit <= vencimiento2)):
                      coeficiente_acum = coeficiente_acum + interes;
                      fecha_punit = vencimiento2
                      vencimiento = vencimiento2

                if ((fecha_punit > vencimiento2) and (fecha_punit <= (vencimiento + relativedelta(days=ven2)))):
                      coeficiente_acum = coeficiente_acum + interes_2
                      fecha_punit = vencimiento + relativedelta(days=ven2)
                      vencimiento = vencimiento + relativedelta(days=ven2)

                if (fecha_punit > (vencimiento + relativedelta(days=ven2))):
                      coeficiente_acum = coeficiente_acum + interes_2
                      vencimiento = vencimiento + relativedelta(days=ven2)

                # if (fecha_punit == vencimiento):
                #   coeficiente_acum = 0;
                #   fecha_punit = vencimiento
                #   vencimiento = vencimiento

                # if settings.DEBUG:
                #     print coeficiente_acum
                #     print fecha_punit
                #     print vencimiento
                #     print "HASTA ACA"

                interes = Configuracion.objects.get(id=settings.MUNI_ID).punitorios
                tipo_interes = Configuracion.objects.get(id=settings.MUNI_ID).tipo_punitorios
                if interes == None:           
                   interes = 0
                   
                if tipo_interes == None:            
                   tipo_interes = 1
                
                interes_especial= True

                if tipo_interes == 2:
                    try:
                        dias = (fecha_punit - vencimiento).days
                    except:
                        dias = 0
                    if dias < 0:
                        dias = 0

                    porc =  (interes / 30 ) * dias

                #MENSUAL
                elif tipo_interes == 1:
                    try:
                        meses = (fecha_punit - vencimiento).days / 30
                    except:
                        meses = 0
                    if meses < 0:
                        meses = 0 
                    porc =  (interes * meses)        

                if (porc < 0):
                    porc = 0
                    coeficiente_acum = 0

                coeficiente_acum = coeficiente_acum + porc
                porc = coeficiente_acum
                
                if (porc < 0):
                    porc=0

                # if settings.DEBUG:
                #     print dias
                #     print porc
                #     print coeficiente_acum
                #     print vencimiento
                #     print vencimiento2
                #     print fecha_punit
      
        else:
            try:
                dias = (fecha_punit - vencimiento).days
            except:
                dias = 0
            if dias < 0:
                dias = 0 
            porc =  (interes / 30 ) * dias
        
        if porc < 0:
            porc = 0
        if settings.DEBUG:
              print 'Interes:'+str(interes)+' TipoInteres:'+str(tipo_interes)+' Meses:'+str(meses)+' Dias:'+str(dias)+' Porc: '+str(porc)+' Venc: '+str(vencimiento)+' FechaPunit: '+str(fecha_punit)
        
        try:
            saldo=cuota.saldo
            if saldo==0:
                b = DriBoleta.objects.get(id_cuota=cuota)                            
                saldo = b.total
                
        except:
            saldo=0

        total = saldo * (porc)
        
            
    except:
        return HttpResponse('Error') # incorrect post
    return total

@login_required 
def verDDJJDrei(request):        
       
    try:
        sitio = Configuracion.objects.get(id=settings.MUNI_ID)
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
                boletas = boletas.filter(id_cuota__id_responsable__nombre__icontains=contribuyente)
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
            'id_boleta__id_cuota__id_responsable__nombre','id_boleta__id_cuota__padron','id_actividad','activ_descr','base','alicuota','minimo','impuesto').order_by('id')
        
                    
    if (request.POST.get('submit') == 'Imprimir') and boleta_detalles:
        context = Context() 
        fecha = datetime.today()                  
        return render_to_pdf_response(request,'drei/reporte_ddjj.html',locals())  
    else:
        return render_to_response('municipio.html',locals(),context_instance=RequestContext(request) )      

@login_required 
def EliminarBoleta(request,idb):
    try:
        boleta = DriBoleta.objects.get(id_boleta=idb)  
        cuota = boleta.id_cuota
        if boleta:
            boleta.delete()
        messages.add_message(request, messages.SUCCESS,u'¡La Boleta/Rectif. fué eliminada exitosamente!.')
        return HttpResponseRedirect(reverse('ver_cuotas', kwargs={'idp':cuota.id_padron}))
    except:
        return HttpResponseRedirect(reverse('padrones_responsable'))