# Generated by Django 4.2.11 on 2024-05-01 14:48

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0051_merge_20240501_1323"),
    ]

    operations = [
        migrations.CreateModel(
            name="WindTurbine2Planned",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, null=True)),
                ("operator", models.CharField(max_length=255, null=True)),
                ("city", models.CharField(max_length=50, null=True)),
                ("zip_code", models.CharField(max_length=50, null=True)),
                ("commissioning_date", models.CharField(max_length=50, null=True)),
                ("capacity_net", models.FloatField(null=True)),
                ("hub_height", models.FloatField(null=True)),
                ("rotor_diameter", models.FloatField(null=True)),
                ("status", models.CharField(max_length=50, null=True)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    "mun_id",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="map.municipality"),
                ),
            ],
            options={
                "verbose_name": "Windenergieanlage (geplant)",
                "verbose_name_plural": "Windenergieanlagen (geplant)",
            },
        ),
        migrations.CreateModel(
            name="WindTurbine2Operating",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, null=True)),
                ("operator", models.CharField(max_length=255, null=True)),
                ("city", models.CharField(max_length=50, null=True)),
                ("zip_code", models.CharField(max_length=50, null=True)),
                ("commissioning_date", models.CharField(max_length=50, null=True)),
                ("capacity_net", models.FloatField(null=True)),
                ("hub_height", models.FloatField(null=True)),
                ("rotor_diameter", models.FloatField(null=True)),
                ("status", models.CharField(max_length=50, null=True)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    "mun_id",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="map.municipality"),
                ),
            ],
            options={
                "verbose_name": "Windenergieanlage (in Betrieb)",
                "verbose_name_plural": "Windenergieanlagen (in Betrieb)",
            },
        ),
        migrations.CreateModel(
            name="WindTurbine2Approved",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, null=True)),
                ("operator", models.CharField(max_length=255, null=True)),
                ("city", models.CharField(max_length=50, null=True)),
                ("zip_code", models.CharField(max_length=50, null=True)),
                ("commissioning_date", models.CharField(max_length=50, null=True)),
                ("capacity_net", models.FloatField(null=True)),
                ("hub_height", models.FloatField(null=True)),
                ("rotor_diameter", models.FloatField(null=True)),
                ("status", models.CharField(max_length=50, null=True)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    "mun_id",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="map.municipality"),
                ),
            ],
            options={
                "verbose_name": "Windenergieanlage (genehmigt)",
                "verbose_name_plural": "Windenergieanlagen (genehmigt)",
            },
        ),
    ]
