from rest_framework import serializers
from .models import docentes, File, Serie
from datetime import datetime
from django.db.models.fields import *
import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class DocenteSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    nombre = serializers.CharField()
    apellidos = serializers.CharField()
    sexo = serializers.CharField()
    correo = serializers.EmailField()
    nacionalidad = serializers.CharField()
    estado = serializers.ReadOnlyField()
    #file = serializers.FileField()
    imagen = serializers.ImageField()
    #titulo = serializers.FileField()
    #diplomado = serializers.FileField()
    #maestria = serializers.FileField()
    #doctorado = serializers.FileField()
    actual = serializers.ReadOnlyField()
    codigoS = serializers.ReadOnlyField()

    def create(self, validated_data):
        Instance = docentes()
        Instance.nombre = validated_data.get('nombre',Instance.nombre)
        Instance.apellidos = validated_data.get('apellidos',Instance.apellidos)
        Instance.sexo = validated_data.get('sexo',Instance.sexo)
        Instance.correo = validated_data.get('correo',Instance.correo)
        Instance.nacionalidad = validated_data.get('nacionalidad',Instance.nacionalidad)
        Instance.imagen = validated_data.get('imagen',Instance.imagen)
        Instance.save()
        return Instance

class FileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    nombre = serializers.CharField()
    apellidos = serializers.CharField()
    sexo = serializers.CharField()
    correo = serializers.EmailField()
    nacionalidad = serializers.CharField()
    estado = serializers.ReadOnlyField()
    codigoSecreto = serializers.ReadOnlyField()

    class Meta:
        model = File
        fields = "__all__"

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']




####Webflix

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = ('id', 'name', 'release_date', 'rating', 'category','imagen')
