# Generated by Django 4.2.11 on 2024-04-30 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0046_pvgroundareas"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pvgroundareas",
            name="year",
            field=models.BigIntegerField(null=True),
        ),
    ]
