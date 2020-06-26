"""PG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.docente.views import Home
from django.conf import settings
from django.conf.urls.static import static
from api.api import docenteAPI
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.usuarios.views import Login, logoutUsuario
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/1.0/create_docente',docenteAPI.as_view(),name = 'api_create_docente'),
    path('',include(('apps.docente.urls','docente'))),
    path('api1/', include('api.urls')),
    path('upload/', include('api.urls')),
    path('docente/',include(('apps.docente.urls','docente'))),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('home/',Home,name = 'index'),
    path('gallery/', include('apps.docente.urls')),


    ###
    #path('', include('api.urls')),
    path('web/', include(('api.urls','web'))),
    ##rest
    path('uploadD/', login_required(include('apps.docente.urls'))),
    path('respuesta/',include(('apps.docente.urls','respuesta'))),


    ##login
    #path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/',Login.as_view(), name = 'login'),
    path('logout/',login_required(logoutUsuario),name = 'logout'),


    ##allauth
    path('accounts/',include('allauth.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
