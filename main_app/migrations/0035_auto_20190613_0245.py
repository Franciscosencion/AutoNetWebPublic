# Generated by Django 2.1 on 2019-06-13 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0034_auto_20190613_0226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deviceinterfaces',
            old_name='interfaces_type',
            new_name='interface_type',
        ),
    ]
