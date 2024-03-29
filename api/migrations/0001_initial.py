# Generated by Django 2.2.12 on 2020-04-14 05:14

import ckeditor.fields
import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='docentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombres')),
                ('apellidos', models.CharField(blank=True, max_length=50, verbose_name='Apellidos')),
                ('sexo', models.CharField(choices=[('MASCULINO', 'Masculino'), ('FEMENINO', 'Femenino'), ('PREFIERO NO DECIRLO', 'Prefiero no decirlo')], default='MASCULINO', max_length=30, verbose_name='Sexo')),
                ('correo', models.EmailField(blank=True, max_length=30, verbose_name='Correo')),
                ('nacionalidad', models.CharField(blank=True, max_length=30, verbose_name='Nacionalidad')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='fotos')),
                ('titulo', models.FileField(blank=True, upload_to='docs', verbose_name='Titulo en provision nacional')),
                ('diplomado', models.FileField(blank=True, upload_to='docs', verbose_name='Titulo de diplomado')),
                ('maestria', models.FileField(blank=True, upload_to='docs', verbose_name='Titulo de maestria')),
                ('doctorado', models.FileField(blank=True, upload_to='docs', verbose_name='Titulo de doctorado')),
                ('actual', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de creación')),
                ('comentarios', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('codigoS', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, verbose_name='Nombres')),
                ('apellidos', models.CharField(blank=True, max_length=50, verbose_name='Apellidos')),
                ('sexo', models.CharField(choices=[('MASCULINO', 'Masculino'), ('FEMENINO', 'Femenino'), ('PREFIERO NO DECIRLO', 'Prefiero no decirlo')], default='MASCULINO', max_length=30, verbose_name='Sexo')),
                ('correo', models.EmailField(blank=True, max_length=30, verbose_name='Correo')),
                ('nacionalidad', models.CharField(blank=True, max_length=30, verbose_name='Nacionalidad')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('file', models.FileField(upload_to='')),
                ('codigoSecreto', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('rating', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[('horror', 'Horror'), ('comedy', 'Comedy'), ('action', 'Action'), ('drama', 'Drama')], max_length=10)),
            ],
        ),
    ]
