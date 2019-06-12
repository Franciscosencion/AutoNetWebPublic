# Generated by Django 2.1 on 2019-06-12 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0031_auto_20190611_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinterfaces',
            name='device',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='device_interfaces', to='main_app.Devices'),
        ),
        migrations.AlterField(
            model_name='devicevlans',
            name='device',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vlans', to='main_app.Devices'),
        ),
    ]
