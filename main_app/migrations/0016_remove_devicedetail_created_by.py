# Generated by Django 2.1 on 2019-05-24 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_devicedetail_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicedetail',
            name='created_by',
        ),
    ]
