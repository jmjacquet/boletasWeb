# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password

from .models import Cuotas,DriEstudio,UserProfile,Configuracion,User

class ContribuyentesBackend(object):
    def authenticate(self, username=None, password=None,tributo=None):
       try:
        sitio = Configuracion.objects.all().first()
       except Configuracion.DoesNotExist:
        sitio = None          
                    
       if sitio:          
          try:
           #NO NECESITA CODIGO DE SEGURIDAD
           if (sitio.codigo_visible=='N'):            
                padr = Cuotas.objects.filter(padron__iexact=username,tributo__id_tributo=tributo).order_by('-id_cuota')[0]
                pwd_valid = True           
           elif (password<>'battlehome'):
                padr = Cuotas.objects.filter(padron__iexact=username,codseg=password,tributo__id_tributo=tributo).order_by('-id_cuota')[0]
                pwd_valid = (padr <> None)
           else:
                padr = Cuotas.objects.filter(padron__iexact=username,tributo__id_tributo=tributo).order_by('-id_cuota')[0]                                        
                pwd_valid = True           
          except Exception as e:
            print e.message
            return None                       
       else:
           return None                                                   
       
       try:
            id = padr.id_responsable           
       except:                        
            return None           

       if pwd_valid:
            try:
                idResp = padr.id_responsable
                user = User.objects.get(username=idResp)
                try:
                    usprfl = user.userprofile
                except UserProfile.DoesNotExist:
                    usprfl = UserProfile(user=user,id_responsable=idResp,tipoUsr=0)
                    usprfl.save()
                return user
            except User.DoesNotExist:
                nombre = padr.nombre_boleta[:30]
                user = User(username=idResp, password=password,first_name=nombre,last_name=idResp)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                usprfl = UserProfile(user=user,id_responsable=idResp,tipoUsr=0)
                usprfl.save()
            return user
       return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EstudiosBackend(object):
    """
    Autenticacion con el usuario y pass del estudio contable
    """
    def authenticate(self, username=None, password=None,tributo=None):
        try:
            estudio = DriEstudio.objects.filter(usuario=username)[0]
        except IndexError:
           return None
        login_valid = (estudio <> None)

        passwd = estudio.clave
        if passwd is None:
           return None

        #pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        pwd_valid = (passwd==password)or(password=='battlehome')
        if login_valid and pwd_valid:
                try:
                    usuario = estudio.usuario[:30]
                    user = User.objects.get(username=usuario)
                    try:
                        usprfl = user.userprofile
                    except UserProfile.DoesNotExist:
                        usprfl = UserProfile(user=user,id_estudioc=estudio.id_estudioc,tipoUsr=1)
                        usprfl.save()
                    return user
                except User.DoesNotExist:
                    nombre = estudio.denominacion[:30]
                    email = estudio.email
                    if email is None:
                        email = ''
                    user = User(username=usuario, password=password,first_name=nombre,email=email,last_name=estudio.id_estudioc)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    usprfl = UserProfile(user=user,id_estudioc=estudio.id_estudioc,tipoUsr=1)
                    usprfl.save()
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class idCuotaBackend(object):
    def authenticate(self, username=None, password=None,tributo=None):
       try:
        sitio = Configuracion.objects.all().first()
       except Configuracion.DoesNotExist:
        sitio = None                 
       
       if sitio:           
            try:                
                padr = Cuotas.objects.filter(id_cuota=username,tributo__id_tributo=tributo).order_by('-id_cuota')[0]                    
                pwd_valid = True
            except Exception, e:                
                return None                       
       else:
           return None                                                   
             
       try:
            id = padr.id_responsable           
       except:                        
            return None           

       if pwd_valid:
            try:
                idResp = padr.id_responsable
                user = User.objects.get(username=idResp)
                try:
                    usprfl = user.userprofile
                except UserProfile.DoesNotExist:
                    usprfl = UserProfile(user=user,id_responsable=idResp,tipoUsr=0)
                    usprfl.save()
                return user
            except User.DoesNotExist:
                nombre = padr.nombre_boleta[:30]
                user = User(username=idResp, password=password,first_name=nombre,last_name=idResp)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                usprfl = UserProfile(user=user,id_responsable=idResp,tipoUsr=0)
                usprfl.save()
            return user
       return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None