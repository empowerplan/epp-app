# Generated by Django 3.2.25 on 2024-03-15 14:25

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0032_rename_potentialareawindstp2027vr_potentialareawindstp2024vr'),
    ]

    operations = [
        migrations.CreateModel(
            name='NaturePark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
