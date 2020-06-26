from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombres,apellidos,password=None):
        if not email:
            raise ValueError('No ingreso correo')

        usuario = self.model(
            username=username,
            nombres=nombres,
            apellidos = apellidos,
            email=self.normalize_email(email),
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,username,email,nombres,apellidos,password):
        usuario = self.create_user(
            email,
            username=username,
            nombres=nombres,
            apellidos = apellidos,
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Mensaje(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=50, blank= True)

    class Meta: #Metadatos
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['id']

    def __str__(self):
        return self.nombre

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario:',unique=True,max_length=200)
    email = models.EmailField('Correo',unique=True,blank=True,max_length=250)
    nombres = models.CharField('Nombre',max_length=200,blank=True,null=True)
    apellidos = models.CharField('Apellidos',max_length=200,blank=True,null=True)
    imagen = models.ImageField('Imagen',upload_to='perfil/',height_field=None,width_field=None,max_length=200,blank=True,null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_tipo = models.CharField('Tipo',max_length=30,
                            choices=(('DIRECTOR','Director'),('COORDINADOR GENERAL','Coordinador general'),
                                     ('ENCARGADA DE PLATAFORMA','Encargada de plataforma'),('FACILITADOR DE PROGRAMAS','Facilitador de programas'),
                                     ('ENCARGADA DE FINANZAS','Encargada de finanzas'),('SECRETARIA','Secretaria'),
                                     ('DOCENTE','Docente'),('CURSANTE','Cursante')),default='CURSANTE')
    usuario_administrador = models.BooleanField(default=False)
    mensaje_usuario = models.ForeignKey(Mensaje,on_delete=models.CASCADE, null=True)
    objects = UsuarioManager()


    class Meta: #Metadatos
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombres','apellidos']

    def __str__(self):
        return f'{self.nombres},{self.apellidos}'

    def has_perm(self,perm,ob=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador


