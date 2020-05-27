# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from .views import login,logout,volverHome

urlpatterns = [    
    url(r'^', include('tadese.urls')),    
    url(r'^api/v1/', include('api.urls')),
    url(r'^login/$', login,name="login"),
    url(r'^logout/$', logout,name="logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:    
	import debug_toolbar
	(?# urlpatterns += url(r'^__debug__/', include(debug_toolbar.urls)),)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler500 = volverHome
handler404 = volverHome