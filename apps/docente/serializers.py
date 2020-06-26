from .models import *
from rest_framework import serializers


class docenteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    nombre = serializers.CharField()
    apellidos = serializers.CharField()
    sexo = serializers.CharField()
    correo = serializers.EmailField()
    nacionalidad = serializers.CharField()
    estado = serializers.ReadOnlyField()
    codigoSecreto = serializers.ReadOnlyField()

    class Meta:
        model = docente
        fields = "__all__"

class cursanteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    nombre = serializers.CharField()
    apellidos = serializers.CharField()
    sexo = serializers.CharField()
    correo = serializers.EmailField()
    nacionalidad = serializers.CharField()
    estado = serializers.ReadOnlyField()
    codigoSecreto = serializers.ReadOnlyField()

    class Meta:
        model = Cursante
        fields = "__all__"

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = docente
        fields = "__all__"
