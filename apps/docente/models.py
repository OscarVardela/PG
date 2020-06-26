from django.db import models
from datetime import datetime
from django.db.models.fields import *
import uuid
from ckeditor.fields import RichTextField


import qrcode
from io import StringIO

from django.db import models
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

import qrcode  # Importamos el modulo necesario para trabajar con codigos

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from apps.usuarios.models import *

# Create your models here.

class programas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombres',max_length=50, blank= True)
    horas = models.CharField('Horas',max_length=50, blank= True)
    creditos = models.CharField('Creditos',max_length=50, blank= True)
    costo = models.FloatField('Costo',max_length=200,blank=False, null=True)
    imagen = models.ImageField(blank=True, null=True)
    fecha_inicio = models.DateField('Fecha de inicio',default=datetime.now, blank=False)
    fecha_final = models.DateField('Fecha de culminación',default=datetime.now, blank=False)
    tipo = models.CharField('Tipo de programa académico',max_length=60,
                            choices=(('DIPLOMADO','Diplomado'),('MAESTRIA','Maestría'),('DOCTORADO','Doctorado'),
                                     ('POSDOCTORADO','Posdoctorado'),('CURSO DE EDUCACION CONTINUA','Curso de educacion continua')),
                              default='DIPLOMADO')

    class Meta: #Metadatos
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class modulos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombres',max_length=50, blank= True)
    horas = models.CharField('Horas',max_length=100,blank=True)
    id_programas=models.ForeignKey(programas,on_delete=models.CASCADE)

    class Meta: #Metadatos
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class docente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombres',max_length=50, blank= True)
    apellidos = models.CharField('Apellidos',max_length=50, blank=True)
    ci = models.IntegerField('Cédula',max_length=30,blank=False,null=True)
    telefono = models.CharField('Telefno',max_length=40,blank=True)
    correo = models.EmailField('Correo',max_length=30, blank=True)
    sexo = models.CharField('Sexo',max_length=30,
                            choices=(('MASCULINO','Masculino'),('FEMENINO','Femenino'),('PREFIERO NO DECIRLO','Prefiero no decirlo')),
                            default='MASCULINO')
    fuerza = models.CharField('Fuerza',max_length=30,
                            choices=(('CÍVIL','civil'),('EJÉCITO','Ejercito'),('FUERZA AÉREA','Fuerza aérea'),('ARMADA','Armada')),
                              default='CÍVIL')
    nacionalidad = models.CharField('Nacionalidad',max_length=30, blank=True)
    estado = models.CharField('Estado',max_length=100,
                              choices=(('APROBADO','Aprobado'),('APROBADO PARCIALMENTE','Aprobado parcialmente'),
                                       ('PARA REVISAR','Para revisar'),('OBSERVADO','Observado')),default='PARA REVISAR')
    estado_seleccion = models.CharField('Estado selección',max_length=100,
                              choices=(('SELECCIONADO','Seleccionado'),('DESCARTADO','Descartado'),('PARA REVISAR','Para revisar')
                                       ),default='PARA REVISAR')
    imagen = models.ImageField(blank=True, null=True)

    curriculum = models.FileField('Curriculum',upload_to='docs',blank=True)
    estado_curriculum=models.CharField('Estado de curriculo',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    titulo = models.FileField('Titulo en provision nacional',upload_to='docs',blank=False)
    estado_titulo=models.CharField('Estado de titulo',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    diplomado = models.FileField('Titulo de diplomado',upload_to='docs',blank=False)
    maestria = models.FileField('Titulo de maestria',upload_to='docs',blank=False)
    estado_maestria=models.CharField('Estado de maestría',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    doctorado = models.FileField('Titulo de doctorado',upload_to='docs',blank=True)
    posdoctorado = models.FileField('Titulo de Posdoctorado',upload_to='docs',blank=True)
    otro = models.FileField('Otros documentos adicionales',upload_to='docs',blank=False,null=True)
    actual = models.DateTimeField('Actual',default=datetime.now,blank=False)
    comentarios = RichTextField(null=True,blank=True)
    codigoS = UUIDField(default=uuid.uuid4,editable=False)
    codigo_titulo=UUIDField(default=uuid.uuid4,editable=False)
    codigo_diplomado=UUIDField(default=uuid.uuid4,editable=False)
    codigo_maestria=UUIDField(default=uuid.uuid4,editable=False)
    id_modulos=models.ManyToManyField(modulos)
    bitacora = models.CharField('Bitacora',max_length=150, blank= True)
    fecha_revision = models.DateTimeField('Fecha de revision',null=True, blank=False)
    documento_observado= RichTextField('Detalles de la observación',null=True,blank=True)
    fecha_aprobacion = models.DateTimeField('Fecha de aprobación',null=True, blank=False)
    id_usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True)


    imagen_thumbnail = ImageSpecField(source='imagen',processors=[ResizeToFill(300,400)],format='JPEG',options={'quality':60})

    class Meta: #Metadatos
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
        ordering = ['nombre']

    def __str__(self):
        #return self.apellidos
        return " ".join([self.nombre, self.apellidos]) #Une los atributos de la clase



class codigo(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField('Codigos',max_length=30, blank=True)
    docente_id = models.OneToOneField(docente, on_delete= models.CASCADE,default="")
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('events.views.details', args=[str(self.id)])

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.get_absolute_url())
        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'events-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qrcode.save(filename, filebuffer)

    class Meta: #Metadatos
        verbose_name = 'Codigo'
        verbose_name_plural = 'Codigos'
        ordering = ['codigo']

    def __str__(self):
        return self.codigo

class Image(models.Model):
   image = models.ImageField(upload_to = 'fotos', default = 'fotos/static/images/no-img.jpg')
   name = models.CharField(max_length=200)

class Cursante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombres',max_length=50, blank= True)
    fecha_de_envio=models.DateTimeField('Fecha de envio',default=datetime.now, blank=False)
    apellidos = models.CharField('Apellidos',max_length=50, blank= True)
    telefono = models.CharField('Teléfono',max_length=50, blank= True)
    ci = models.IntegerField('Cédula',max_length=30,blank=False,null=True)
    sexo = models.CharField('Sexo',max_length=30,
                            choices=(('MASCULINO','Masculino'),('FEMENINO','Femenino'),('PREFIERO NO DECIRLO','Prefiero no decirlo')),default='MASCULINO')
    fuerza = models.CharField('Fuerza',max_length=30,
                            choices=(('CÍVIL','civil'),('EJÉRCITO','Ejercito'),('FUERZA AÉREA','Fuerza aérea'),('ARMADA','Armada')),default='CÍVIL')

    correo = models.EmailField('Correo',max_length=30, blank=True)
    nacionalidad = models.CharField('Nacionalidad',max_length=30, blank=True)
    imagen = models.ImageField(blank=True, null=True)

    titulo = models.FileField('Titulo Nivel nacional',upload_to='docs',blank=True)
    estado_titulo = models.CharField('Estado de titulo',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    solicitud = models.FileField('Solicitud',upload_to='docs',blank=True)
    curriculum = models.FileField('Curriculum',upload_to='docs',blank=True)

    certificado = models.FileField('Certificado de nacimiento',upload_to='docs',blank=True)
    estado_certificado = models.CharField('Estado de certificado',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    formulario = models.FileField('Formulario de admisión',upload_to='docs',blank=True)
    estado_formulario = models.CharField('Estado de formulario',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    cedula = models.FileField('Cedula o pasaporte',upload_to='docs',blank=True)
    estado_cedula = models.CharField('Estado de cedula',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    contrato = models.FileField('Contrato',upload_to='docs',blank=True)
    estado_contrato = models.CharField('Estado de contrato',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    comprobante = models.FileField('Comprobante de pago',upload_to='docs',blank=False)
    estado_comprobante = models.CharField('Estado de comprobante',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    certificado_no_adeudo = models.FileField('Certificado de no adeudo',upload_to='docs',blank=True)
    estado_no_adeudo = models.CharField('Estado de no adeudo',max_length=100,
                              choices=(('APROBADO','Aprobado'),('OBSERVADO','Observado')),default='OBSERVADO')

    luzagua = models.FileField('Factura de luz/agua',upload_to='docs',blank=True)
    croquis = models.FileField('Croquis',upload_to='docs',blank=True)

    estado = models.CharField('Estado',max_length=100,
                              choices=(('APROBADO','Aprobado'),('APROBADO PARCIALMENTE','Aprobado parcialmente'),
                                       ('APROBADO FINANZAS','Aprobado finanzas'),
                                       ('PARA REVISAR','Para revisar')),default='PARA REVISAR')

    codigoS = UUIDField(default=uuid.uuid4,editable=False)
    historial = RichTextField(null=True,blank=True)
    bitacora = models.CharField('Bitacora',max_length=150, blank= True)
    bitacora_finanzas = models.CharField('Bitacora',max_length=150, blank= True)
    fecha_envio = models.DateTimeField('Fecha de envio',default=datetime.now,blank=False)
    fecha_envio_baucher = models.DateTimeField('Fecha de envio',default=datetime.now,blank=False)
    fecha_revision = models.DateTimeField('Fecha de revision',null=True, blank=False)
    fecha_revision_finanzas = models.DateTimeField('Fecha de revision finanzas',null=True, blank=False)
    documento_observado= RichTextField(null=True,blank=True)
    fecha_aprobacion = models.DateTimeField('Fecha de aprobación',null=True, blank=False)
    id_programas=models.ForeignKey(programas,on_delete=models.CASCADE,null=True)
    id_usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True)

    class Meta: #Metadatos
        verbose_name = 'Cursante'
        verbose_name_plural = 'CUrsantes'
        ordering = ['nombre']

    def __str__(self):
        #return self.apellidos
        return " ".join([self.nombre, self.apellidos]) #Une los atributos de la clase

class interno(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=50, blank= True)
    detalle = RichTextField(null=True,blank=True)
    documento = models.FileField('Documento',upload_to='docs',blank=True)
    remitente = models.CharField('Remitente',blank=True,max_length=200)
    fecha = models.DateField('Fecha de creación',default=datetime.now, blank=False)
    fecha_recepcion = models.DateTimeField('Fecha de recepción',null=True, blank=False)
    receptor = models.CharField('Receptor',blank=True,max_length=200)
    area = models.CharField('Area Interna',max_length=30,
                            choices=(('DIRECTOR','Director'),('COORDINADOR GENERAL','Coordinador general'),
                                     ('ENCARGADA DE PLATAFORMA','Encargada de plataforma'),('FACILITADOR DE PROGRAMAS','Facilitador de programas'),
                                     ('ENCARGADA DE FINANZAS','Encargada de finanzas'),('SECRETARIA','Secretaria')),default='CÍVIL')
    estado = models.CharField('Estado',max_length=100,
                              choices=(('ACTIVO','Activo'),('ARCHIVADO','Archivado')),default='ACTIVO')


    class Meta: #Metadatos
        verbose_name = 'Interno'
        verbose_name_plural = 'Internos'
        ordering = ['nombre']

    def __str__(self):
        #return self.apellidos
        return self.nombre
