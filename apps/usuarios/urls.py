from django.urls import path
from .views import ListadoUsuario,RegistrarUsuario, EditarUsuario
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('listado_usuarios/',login_required(ListadoUsuario.as_view()),name = 'listar_usuarios'),
    path('registrar_usuario/',login_required(RegistrarUsuario.as_view()),name = 'registrar_usuario'),
    path('actualizar_usuario/<int:pk>',login_required(EditarUsuario.as_view()),name = 'actualizar_usuario'),
]

## URLS de vistas implicitas
urlpatterns += [
    path('inicio_usuarios/',login_required(TemplateView.as_view(
                        template_name = 'usuarios/listar_usuario.html'
                        )
                    ),name = 'inicio_usuarios'),
]
