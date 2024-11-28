# Generated by Django 4.2.16 on 2024-11-26 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0056_alter_waterfirstorder_geom'),
    ]

    operations = [
        migrations.AddField(
            model_name='potentialareawindstp2024vr',
            name='municipality_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='map.municipality'),
        ),
        migrations.AddField(
            model_name='potentialareawindstp2024vr',
            name='vr_wen_nr',
            field=models.CharField(max_length=255, null=True),
        ),
    ]