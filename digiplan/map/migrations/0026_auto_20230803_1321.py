# Generated by Django 3.2.20 on 2023-08-03 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0025_auto_20230803_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='biomass',
            name='biomass_only',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biomass',
            name='feedin_type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biomass',
            name='flexibility_bonus',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biomass',
            name='fuel',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biomass',
            name='kwk_mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biomass',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biomass',
            name='technology',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biomass',
            name='th_capacity',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='bnetza_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='feedin_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='fuel_other',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='fuels',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='kwk_mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='technology',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='th_capacity',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='combustion',
            name='usage_sector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='gsgk',
            name='kwk_mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='gsgk',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='gsgk',
            name='technology',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='gsgk',
            name='th_capacity',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='gsgk',
            name='type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hydro',
            name='feedin_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hydro',
            name='kwk_mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hydro',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hydro',
            name='plant_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='area_occupied',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='area_type',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='citizens_unit',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='feedin_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='landlord_to_tenant_electricity',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='module_count',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='orientation_primary',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='orientation_secondary',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='site_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pvground',
            name='usage_sector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='area_occupied',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='area_type',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='citizens_unit',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='feedin_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='landlord_to_tenant_electricity',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='module_count',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='orientation_primary',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='orientation_secondary',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='site_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pvroof',
            name='usage_sector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='citizens_unit',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='constraint_deactivation_animals',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='constraint_deactivation_ice',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='constraint_deactivation_shadowing',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='constraint_deactivation_sound_emission',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='constraint_deactivation_sound_emission_day',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='constraint_deactivation_sound_emission_night',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='manufacturer_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='mastr_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='site_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='type_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
