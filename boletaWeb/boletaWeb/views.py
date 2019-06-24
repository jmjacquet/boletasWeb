# -*- coding: utf-8 -*-

from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.shortcuts import *
from settings import *
from django.core.urlresolvers import reverse
from django.contrib import messages
from tadese.models import Configuracion,Cuotas,Tributo,UserProfile
from tadese.utilidades import TRIBUTOS_LOGIN
from django.db.models import Q
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


LOGIN_REDIRECT_URL='/'

def login(request):
    error = None
    LOGIN_REDIRECT_URL='/'
   
    if request.user.is_authenticated():
      return HttpResponseRedirect(LOGIN_REDIRECT_URL)
      
    try:
        sitio = Configuracion.objects.get(id=MUNI_ID)
    except Configuracion.DoesNotExist:
        sitio = None
    if sitio <> None:
      unico_padr = (sitio.ver_unico_padron == 'S')
      #unico_padr = False
      # if MODO_DEBUG == 1:
      #   return render_to_response('mantenimiento.html', {'dirMuni':MUNI_DIR,'sitio':sitio},context_instance=RequestContext(request))

      if sitio.mantenimiento == 1:
        return render_to_response('mantenimiento.html', {'dirMuni':MUNI_DIR,'sitio':sitio},context_instance=RequestContext(request))
    else:
      unico_padr = False

    if request.method == 'POST':
        
        user = authenticate(username=request.POST['username'], password=request.POST['password'],tributo=request.POST['tributo'])
        if user is not None:
          if user.is_active:
            django_login(request, user)
            if user.userprofile.tipoUsr==0:
                request.session["usuario"] = request.POST['username']
                if unico_padr:
                  try:
                        padr = Cuotas.objects.filter(padron=request.POST['username'],estado=0).order_by('-id_cuota')[0]
                        LOGIN_REDIRECT_URL = reverse('ver_cuotas', kwargs={'idp':padr.id_padron})
                  except IndexError:
                        padr = None   
                else:
                  LOGIN_REDIRECT_URL = reverse('padrones_responsable')
            elif user.userprofile.tipoUsr==1:
                LOGIN_REDIRECT_URL = reverse('padrones_estudio')
            elif user.userprofile.tipoUsr==2:
                 LOGIN_REDIRECT_URL = reverse('padrones_responsable')
            return HttpResponseRedirect(LOGIN_REDIRECT_URL)
          else:
          ## invalid login
           error = u'Verifique que:\n. Los datos sean correctos.\n. Posea cuotas generadas en el sistema.'
        else:
          ## invalid login
           error = u'Verifique que:\n. Los datos sean correctos.\n. Posea cuotas generadas en el sistema.'
          #return direct_to_template(request, 'invalid_login.html')
    if error:
      messages.add_message(request, messages.ERROR,u'%s' % (error))

    

    tributos = Tributo.objects.filter()
    
    return render_to_response('index.html', {'dirMuni':MUNI_DIR,'sitio':sitio,'tributos':tributos},context_instance=RequestContext(request))

def login2(request):
    error = None
    LOGIN_REDIRECT_URL='/'
   
    if request.user.is_authenticated():
      return HttpResponseRedirect(LOGIN_REDIRECT_URL)      
    try:
        sitio = Configuracion.objects.get(id=MUNI_ID)
    except Configuracion.DoesNotExist:
        sitio = None

    if request.method == 'POST':        
        user = authenticate(username=request.POST['username'], password=request.POST['password'],tributo=request.POST['tributo'])
        if user is not None:
          if user.is_active:
            django_login(request, user)
            LOGIN_REDIRECT_URL = reverse('padrones_responsable')
            return HttpResponseRedirect(LOGIN_REDIRECT_URL)
          else:
          ## invalid login
           error = u'Verifique que:\n. Los datos sean correctos.\n. Posea cuotas generadas en el sistema.'
        else:
          ## invalid login
           error = u'Verifique que:\n. Los datos sean correctos.\n. Posea cuotas generadas en el sistema.'
          #return direct_to_template(request, 'invalid_login.html')
    if error:
      messages.add_message(request, messages.ERROR,u'%s' % (error))

    tributos = Tributo.objects.filter(Q(id_tributo__lte=7)|Q(id_tributo=10))
    
    return render_to_response('index2.html', {'dirMuni':MUNI_DIR,'sitio':sitio,'tributos':tributos},context_instance=RequestContext(request))


def logout(request):
    request.session.clear()
    django_logout(request)
    return HttpResponseRedirect(LOGIN_URL)

def volverHome(request):
    
    if not request.user.is_authenticated():
      return HttpResponseRedirect(LOGIN_URL)    
   
    if request.user.userprofile.tipoUsr==0:
        LOGIN_REDIRECT_URL = reverse('padrones_responsable')
    elif request.user.userprofile.tipoUsr==1:
        LOGIN_REDIRECT_URL = reverse('padrones_estudio')
    else:
                LOGIN_REDIRECT_URL = reverse('padrones_responsable') 
    
    return HttpResponseRedirect(LOGIN_REDIRECT_URL)

