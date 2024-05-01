# Generated by Django 4.2.11 on 2024-04-30 15:55

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0047_alter_pvgroundareas_year"),
    ]

    operations = [
        migrations.CreateModel(
            name="PVgroundAreasApproved",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("geom", django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ("name", models.CharField(max_length=255, null=True)),
                ("plan_type", models.CharField(max_length=255, null=True)),
                ("plan_status", models.CharField(max_length=255, null=True)),
                ("status", models.CharField(max_length=10, null=True)),
                ("capacity_net", models.FloatField(null=True)),
                ("year", models.BigIntegerField(null=True)),
                ("construction_start_date", models.CharField(max_length=10, null=True)),
                ("construction_end_date", models.CharField(max_length=10, null=True)),
                (
                    "mun_id",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="map.municipality"),
                ),
            ],
            options={
                "verbose_name": "Ground-mounted PV Area",
                "verbose_name_plural": "Ground-mounted PV Areas",
            },
        ),
        migrations.DeleteModel(
            name="PVgroundAreas",
        ),
    ]