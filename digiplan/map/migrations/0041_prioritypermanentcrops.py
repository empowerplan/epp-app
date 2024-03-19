# Generated by Django 3.2.25 on 2024-03-18 13:25

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0040_priorityclimateresistentagri'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriorityPermanentCrops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]