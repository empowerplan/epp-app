# Generated by Django 3.2.25 on 2024-03-18 13:07

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0038_pvgroundcriterianaturemonuments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterfirstorder',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326),
        ),
    ]
