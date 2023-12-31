# Generated by Django 3.2.16 on 2023-02-17 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0012_add_mun_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('value', models.IntegerField(null=True)),
                ('entry_type', models.CharField(max_length=13)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.municipality')),
            ],
        ),
    ]
