# Generated by Django 2.2.12 on 2020-04-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serie',
            name='imagen',
            field=models.ImageField(null=True, upload_to='fotos'),
        ),
    ]
