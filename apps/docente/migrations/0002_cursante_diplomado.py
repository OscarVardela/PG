# Generated by Django 2.2.12 on 2020-06-11 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cursante',
            name='diplomado',
            field=models.FileField(blank=True, upload_to='docs', verbose_name='Titulo de diplomado'),
        ),
    ]
