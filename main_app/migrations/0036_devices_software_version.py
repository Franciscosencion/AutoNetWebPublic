# Generated by Django 2.1 on 2019-06-14 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0035_auto_20190613_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='software_version',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
