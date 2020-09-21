# -*- coding: utf-8 -*-
from django.conf.urls import  include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api.views import APICuotasViewSet,APIBoletasViewSet
# from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token
from rest_framework import routers
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title=u'Documentación de la Web API.')

router = routers.DefaultRouter()
router.register(r'cuotas', APICuotasViewSet)
router.register(r'boletas', APIBoletasViewSet)

urlpatterns = [       
   url('', include(router.urls)),
   # url(r'^token/', obtain_jwt_token, name='token_create'),    
   # url(r'^token-refresh/', refresh_jwt_token,name='token_refresh'),
   # url(r'^token-verify/', verify_jwt_token,name='token_verify'),

   # url(r'^cuotas/(?P<idp>[^/]+)/$', APICuotasListPadron.as_view(),name="api_cuotas_padron"),
   # url(r'^padrones/(?P<idResp>[^/]+)/$', APIPadronesList.as_view(),name="api_padrones"),    

   

   # url(r'^cuota/(?P<idc>[^/]+)/$', APICuota.as_view(),name="api_cuota_ver"),

   url(r'^', schema_view),
   url(r'^auth/', include('rest_framework.urls')),   

]