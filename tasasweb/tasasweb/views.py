# -*- coding: utf-8 -*-
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.shortcuts import *
from .settings import *
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q
from django.template.defaulttags import register
from django.conf import settings
from tadese.models import Configuracion,Cuotas,Tributo,UserProfile
from tadese.utilidades import TRIBUTOS_LOGIN

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def login(request):
    LOGIN_REDIRECT_URL=settings.LOGIN_REDIRECT_URL
    error = None
      
    if request.user.is_authenticated():     
      return volverHome(request)
      
    try:
        sitio = Configuracion.objects.all().first()
    except Configuracion.DoesNotExist:
        sitio = None
    
    if sitio <> None:
      unico_padr = (sitio.ver_unico_padron == 'S')
          
      if sitio.mantenimiento == 1:
        return render(request,'mantenimiento.html', {'dirMuni':MUNI_DIR,'sitio':sitio})
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
                        padr = Cuotas.objects.filter(padron=request.POST['username'],estado=0).order_by('-id_cuota').first()
                        if padr:
                          LOGIN_REDIRECT_URL = reverse('ver_cuotas', kwargs={'idp':padr.id_padron})
                        else:
                          LOGIN_REDIRECT_URL = reverse('padrones_responsable')
                  except:
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
           error = u'Verifique que:\n.Los datos sean correctos.\n.El Padrón posea cuotas generadas en el sistema.'
        else:
          ## invalid login
           error = u'Verifique que:\n.Los datos sean correctos.\n.El Padrón posea cuotas generadas en el sistema.'
          
    if error:
      messages.add_message(request, messages.ERROR,u'%s' % (error))

    tributos = Tributo.objects.all()
    return render(request,'index.html', {'dirMuni':MUNI_DIR,'sitio':sitio,'tributos':tributos})


def logout(request):
    request.session.clear()
    django_logout(request)
    return HttpResponseRedirect(LOGIN_URL)

def recargarLogueo(request):  
  request.user.userprofile.delete()
  error = u'Verifique que:\n. Los datos sean correctos.\n. Posea cuotas generadas en el sistema.'
  messages.add_message(request, messages.ERROR,u'%s' % (error))
  logout(request)
  
def volverHome(request):        
    if not request.user.is_authenticated():
      return redirect(LOGIN_URL)       
    else:      
      if request.user.userprofile.tipoUsr==0:
          LOGIN_REDIRECT_URL = reverse('padrones_responsable')
      elif request.user.userprofile.tipoUsr==1:
          LOGIN_REDIRECT_URL = reverse('padrones_estudio')
      else:
           LOGIN_REDIRECT_URL = reverse('padrones_responsable')       
      return redirect(LOGIN_REDIRECT_URL)    
 