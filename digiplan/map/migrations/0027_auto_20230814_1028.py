# Generated by Django 3.2.20 on 2023-08-14 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0026_auto_20230803_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gsgk',
            name='type',
        ),
        migrations.AddField(
            model_name='gsgk',
            name='unit_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hydro',
            name='kwk_mastr_id',
            field=models.FloatField(null=True),
        ),
    ]
