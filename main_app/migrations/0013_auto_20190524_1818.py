# Generated by Django 2.1 on 2019-05-24 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_auto_20190524_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedetail',
            name='last_modify',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
