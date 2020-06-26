from django.urls import path, include
from .views import *
from .api import *
from .views import *
from rest_framework import routers


urlpatterns = [
    path('', FileUploadView.as_view()),


    path('series/',serie_list),
    path('series/<str:name>',serie_detail),##servicio por nombre de pelicula
    path('file/<str:nombre>',filee_detail),
]
