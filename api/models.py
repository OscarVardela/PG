from django.db import models
from datetime import datetime
from django.db.models.fields import *
import uuid
from ckeditor.fields import RichTextField



class docentes(models.Model):
    nombre = models.CharField('Nombres',max_length=50, blank= True)
    apellidos = models.CharField('Apellidos',max_length=50, blank=True)
    sexo = models.CharField('Sexo',max_length=30,
                            choices=(('MASCULINO','Masculino'),('FEMENINO','Femenino'),('PREFIERO NO DECIRLO','Prefiero no decirlo')),default='MASCULINO')
    correo = models.EmailField('Correo',max_length=30, blank=True)
    nacionalidad = models.CharField('Nacionalidad',max_length=30, blank=True)
    estado = models.BooleanField('Estado', default=True)
    #file = models.FileField(blank=False, null=False)
    imagen = models.ImageField(upload_to='fotos',null=True,blank=True)
    titulo = models.FileField('Titulo en provision nacional',upload_to='docs',blank=True)
    diplomado = models.FileField('Titulo de diplomado',upload_to='docs',blank=True)
    maestria = models.FileField('Titulo de maestria',upload_to='docs',blank=True)
    doctorado = models.FileField('Titulo de doctorado',upload_to='docs',blank=True)
    actual = models.DateTimeField('Fecha de creación',default=datetime.now,blank=False)
    comentarios = RichTextField(blank=True,null=True)
    codigoS = UUIDField(default=uuid.uuid4,editable=False)


class File(models.Model):
    nombre = models.CharField('Nombres',max_length=50, blank= True)
    apellidos = models.CharField('Apellidos',max_length=50, blank=True)
    sexo = models.CharField('Sexo',max_length=30,
                            choices=(('MASCULINO','Masculino'),('FEMENINO','Femenino'),('PREFIERO NO DECIRLO','Prefiero no decirlo')),default='MASCULINO')
    correo = models.EmailField('Correo',max_length=30, blank=True)
    nacionalidad = models.CharField('Nacionalidad',max_length=30, blank=True)
    estado = models.BooleanField('Estado', default=True)
    #file = models.FileField(blank=False, null=False)
    #comentarios = RichTextField(null=True)
    file = models.FileField(blank=False, null=False)
    codigoSecreto = UUIDField(default=uuid.uuid4,editable=False)

    class Meta: #Metadatos
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre





##Webflix
class Serie(models.Model):

    HORROR = 'horror'
    COMEDY = 'comedy'
    ACTION = 'action'
    DRAMA = 'drama'

    CATEGORIES_CHOICES = (
        (HORROR, 'Horror'),
        (COMEDY, 'Comedy'),
        (ACTION, 'Action'),
        (DRAMA, 'Drama'),
    )

    name = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.IntegerField(default=0)
    category = models.CharField(max_length=10, choices=CATEGORIES_CHOICES)
    imagen = models.ImageField(upload_to='fotos',null=True,blank=True)
