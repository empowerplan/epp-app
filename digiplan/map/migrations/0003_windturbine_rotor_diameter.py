# Generated by Django 3.2.16 on 2023-01-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_windturbine'),
    ]

    operations = [
        migrations.AddField(
            model_name='windturbine',
            name='rotor_diameter',
            field=models.FloatField(null=True),
        ),
    ]
