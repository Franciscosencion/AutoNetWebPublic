# Generated by Django 2.1 on 2019-06-11 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0028_auto_20190611_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInterfaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interfaces', models.CharField(blank=True, max_length=100, null=True)),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='main_app.Devices')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceVlans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vlan_name', models.CharField(blank=True, max_length=200, null=True)),
                ('vlan_id', models.IntegerField(blank=True, null=True)),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vlans', to='main_app.Devices')),
            ],
        ),
        migrations.RemoveField(
            model_name='devicedetail',
            name='interfaces',
        ),
        migrations.RemoveField(
            model_name='devicedetail',
            name='vlans',
        ),
    ]