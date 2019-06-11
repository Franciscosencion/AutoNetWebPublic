# Generated by Django 2.1 on 2019-06-11 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_devices_device_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='operating_system',
            field=models.CharField(choices=[('1', 'CISCO IOS'), ('2', 'CISCO IOS-XE'), ('3', 'CISCO IOS-XR'), ('4', 'CISCO NX-OS')], default=(('1', 'CISCO IOS'), ('2', 'CISCO IOS-XE'), ('3', 'CISCO IOS-XR'), ('4', 'CISCO NX-OS')), max_length=10),
        ),
    ]