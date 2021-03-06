# Generated by Django 2.2.12 on 2020-06-16 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docente', '0007_cursante_estado_certificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cursante',
            name='estado_cedula',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('OBSERVADO', 'Observado')], default='OBSERVADO', max_length=100, verbose_name='Estado de titulo'),
        ),
        migrations.AddField(
            model_name='cursante',
            name='estado_comprobante',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('OBSERVADO', 'Observado')], default='OBSERVADO', max_length=100, verbose_name='Estado de titulo'),
        ),
        migrations.AddField(
            model_name='cursante',
            name='estado_contrato',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('OBSERVADO', 'Observado')], default='OBSERVADO', max_length=100, verbose_name='Estado de titulo'),
        ),
        migrations.AddField(
            model_name='cursante',
            name='estado_formulario',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('OBSERVADO', 'Observado')], default='OBSERVADO', max_length=100, verbose_name='Estado de titulo'),
        ),
        migrations.AddField(
            model_name='cursante',
            name='estado_no_adeudo',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('OBSERVADO', 'Observado')], default='OBSERVADO', max_length=100, verbose_name='Estado de titulo'),
        ),
        migrations.AddField(
            model_name='cursante',
            name='estado_titulo',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('OBSERVADO', 'Observado')], default='OBSERVADO', max_length=100, verbose_name='Estado de titulo'),
        ),
        migrations.AlterField(
            model_name='cursante',
            name='estado_certificado',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('OBSERVADO', 'Observado')], default='OBSERVADO', max_length=100, verbose_name='Estado de certificado'),
        ),
    ]
